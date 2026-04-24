#!/usr/bin/env python3
"""
dataset_builder.py — Markdown-to-JSONL Dataset Builder for Unsloth Fine-Tuning

Parses Markdown files (converted from PDFs) into a Hugging Face-compatible
JSONL dataset in ShareGPT conversational format for LLM fine-tuning.

The parser is designed to handle PDF-to-Markdown conversion artifacts where:
- ## headings are page-range markers, not content headings
- Actual section titles are title-cased standalone lines in the body
- Tables of contents appear as numbered lists and should be skipped
- Page footers like "Recording 18" appear throughout

Usage:
    python dataset_builder.py
    python dataset_builder.py --input-dir ./Data --output ./Data/training_data.jsonl
    python dataset_builder.py --max-chunk-chars 3000 --min-section-chars 100
"""

import argparse
import json
import re
import random
from pathlib import Path


# ---------------------------------------------------------------------------
# Question templates — varied to prevent overfitting on a single phrasing
# ---------------------------------------------------------------------------
QUESTION_TEMPLATES = [
    "How do I {topic} on the Blackmagic PYXIS?",
    "Explain {topic} for the Blackmagic PYXIS camera.",
    "What should I know about {topic} on the Blackmagic PYXIS?",
    "Describe {topic} on the Blackmagic PYXIS.",
    "Tell me about {topic} for the Blackmagic PYXIS camera.",
    "Can you explain how {topic} works on the Blackmagic PYXIS?",
    "What is {topic} on the Blackmagic PYXIS?",
    "Give me details about {topic} on the Blackmagic PYXIS camera.",
]

# Seed for reproducibility
random.seed(42)


# ---------------------------------------------------------------------------
# Cleaning helpers
# ---------------------------------------------------------------------------
def clean_body(text: str) -> str:
    """Remove PDF conversion artifacts and normalize whitespace."""
    # Remove page markers like "_Pages 4–4_" or "_Pages 25–26_"
    text = re.sub(r"_Pages?\s*\d+[\s–\-]+\d+_", "", text)
    # Remove standalone page footers like "Recording 18", "Settings 75"
    # These are lines that end with just a number and have a known section name
    text = re.sub(
        r"\n[A-Z][A-Za-z &\-'()]+ \d{1,4}\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )
    # Remove horizontal rules
    text = re.sub(r"\n-{3,}\n", "\n", text)
    # Remove ## page-range headings
    text = re.sub(r"\n##\s+[^\n]+\n", "\n", text)
    # Normalize whitespace
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_toc_line(line: str) -> bool:
    """Check if a line looks like a table-of-contents entry (title + page number)."""
    stripped = line.strip()
    # Pattern: text followed by a number at the end (TOC entries)
    # e.g., "Getting Started 6", "Attaching a Lens 6", "CFexpress Cards 10"
    if re.match(r"^[A-Z][A-Za-z &\-'/()\.]+ \d{1,4}$", stripped):
        # Single line ending in a number — likely TOC
        return True
    return False


# API documentation table headers that repeat throughout and should NOT be headings
HEADING_BLACKLIST = {
    "Name Type Description",
    "Response",
    "Parameters",
    "Stops Above",
    "Stops Below",
    "Total Stops",
    "Stops Above Middle Grey",
    "Stops Below Middle Grey",
    "CAM",
}


def is_api_endpoint(line: str) -> bool:
    """Check if a line is a REST API endpoint definition."""
    stripped = line.strip()
    return bool(re.match(r"^(GET|PUT|POST|DELETE|PATCH)\s+/", stripped))


def is_section_heading(line: str, next_line: str = "") -> bool:
    """
    Detect lines that act as section headings in the PDF-converted markdown.
    
    Section headings in this document are standalone title-cased lines that:
    - Start with an uppercase letter
    - Are relatively short (< 80 chars)
    - Don't end with sentence-ending punctuation
    - Are followed by body text (not another heading or a number)
    - Consist of properly capitalized words
    - Are NOT in the blacklist of API doc table headers
    """
    stripped = line.strip()

    if not stripped or len(stripped) > 80 or len(stripped) < 3:
        return False

    # Check blacklist
    if stripped in HEADING_BLACKLIST:
        return False

    # API endpoints are headings
    if is_api_endpoint(stripped):
        return True

    # Must start with uppercase
    if not stripped[0].isupper():
        return False

    # Must not end with sentence punctuation
    if stripped.endswith((".", ",", ":", ";", "!")):
        return False

    # Must not be a numbered item
    if re.match(r"^\d+\s", stripped):
        return False

    # Must not start with common non-heading indicators
    if stripped.startswith(("*", "-", ">", "|", "TIP ", "NOTE ", "http", "www", "©")):
        return False

    # Must not be all-caps boilerplate (like warranty text)
    if stripped.isupper() and len(stripped) > 20:
        return False

    # Must look like a title — predominantly capitalized words
    words = stripped.split()
    if len(words) < 1 or len(words) > 12:
        return False

    # At least the first word must be capitalized
    if not words[0][0].isupper():
        return False

    # Should match title-like pattern: words with some lowercase connectors
    title_pattern = re.match(
        r"^[A-Z][A-Za-z0-9]*(?:\s+(?:[a-z]{1,4}|[A-Z/][A-Za-z0-9\-/.'&()]*|[0-9]+[A-Za-z]*))*$",
        stripped,
    )
    if not title_pattern:
        return False

    # Should NOT be a TOC line (heading followed by page number)
    if is_toc_line(stripped):
        return False

    return True


# ---------------------------------------------------------------------------
# Content section parser
# ---------------------------------------------------------------------------
class ContentSection:
    """A logical section of manual content with a heading and body."""

    def __init__(self, heading: str, body: str):
        self.heading = heading
        self.body = body

    def __repr__(self):
        return f"ContentSection({self.heading!r}, body_len={len(self.body)})"


def identify_toc_region(lines: list[str]) -> tuple[int, int]:
    """
    Find the table of contents region by looking for dense clusters of
    TOC-like lines (title + page number).
    """
    toc_start = -1
    toc_end = -1
    consecutive_toc = 0

    for i, line in enumerate(lines):
        if is_toc_line(line.strip()):
            if consecutive_toc == 0:
                candidate_start = i
            consecutive_toc += 1
            if consecutive_toc >= 5:
                # We're in a TOC region
                if toc_start == -1:
                    toc_start = candidate_start
                toc_end = i
        else:
            if line.strip():  # Only reset on non-empty lines
                consecutive_toc = 0

    return toc_start, toc_end


def parse_content_sections(text: str) -> list[ContentSection]:
    """
    Parse the cleaned document text into content sections based on
    inline section headings (title-cased standalone lines).
    """
    lines = text.splitlines()
    
    # First, identify and skip TOC regions
    toc_start, toc_end = identify_toc_region(lines)

    sections: list[ContentSection] = []
    current_heading = "Introduction"
    current_body_lines: list[str] = []
    in_toc = False

    for i, line in enumerate(lines):
        # Skip TOC region
        if toc_start <= i <= toc_end:
            continue

        stripped = line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # Check if this is a section heading (title-cased line or API endpoint)
        if is_section_heading(stripped, next_line):
            # Save previous section if it has content
            body = "\n".join(current_body_lines).strip()
            if body and len(body) >= 30:
                sections.append(ContentSection(current_heading, body))

            current_heading = stripped
            current_body_lines = []
        else:
            # Skip lines that look like TOC entries even outside the main TOC
            if is_toc_line(stripped) and not current_body_lines:
                continue
            current_body_lines.append(line)

    # Final section
    body = "\n".join(current_body_lines).strip()
    if body and len(body) >= 30:
        sections.append(ContentSection(current_heading, body))

    return sections


# ---------------------------------------------------------------------------
# Post-processing: merge very short sections, chunk long ones
# ---------------------------------------------------------------------------
def chunk_text(text: str, max_chars: int, heading: str = "") -> list[str]:
    """Split text into chunks on paragraph boundaries, with single-line fallback."""
    if len(text) <= max_chars:
        return [text]

    # Try splitting on double newlines first
    paragraphs = re.split(r"\n\n+", text)

    # If any paragraph is still too long, split it on single newlines
    expanded = []
    for para in paragraphs:
        if len(para) > max_chars:
            expanded.extend(para.split("\n"))
        else:
            expanded.append(para)
    paragraphs = expanded

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) > max_chars and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(para)
        current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))

    # Add context to continuation chunks
    if heading and len(chunks) > 1:
        for i in range(1, len(chunks)):
            chunks[i] = f"(Continued — {heading})\n\n{chunks[i]}"

    return chunks


# ---------------------------------------------------------------------------
# Question generation
# ---------------------------------------------------------------------------
def heading_to_topic(heading: str) -> str:
    """Convert a section heading to a natural-language topic phrase."""
    topic = heading.strip()
    # Don't lowercase proper nouns and acronyms
    skip_lower = {
        "Blackmagic", "PYXIS", "DaVinci", "Resolve", "CFexpress",
        "USB-C", "SDI", "HDMI", "LUT", "LUTs", "RAW", "LoRA",
        "Bluetooth", "WiFi", "HDR", "EVF", "PL", "EF", "ISO",
        "URSA", "Cine", "API", "REST", "XML", "ISED", "FCC",
        "Mac", "Windows", "Linux", "Cooke", "Adobe", "Avid",
        "Premiere", "Pro", "Final", "Cut",
    }
    words = topic.split()
    if words and words[0] not in skip_lower:
        words[0] = words[0][0].lower() + words[0][1:]
    return " ".join(words)


def generate_question(heading: str, idx: int) -> str:
    """Pick a question template deterministically based on index."""
    topic = heading_to_topic(heading)
    template = QUESTION_TEMPLATES[idx % len(QUESTION_TEMPLATES)]
    return template.format(topic=topic)


# ---------------------------------------------------------------------------
# Build the dataset
# ---------------------------------------------------------------------------
def build_qa_pairs(
    sections: list[ContentSection],
    max_chunk_chars: int = 2000,
    min_section_chars: int = 50,
) -> list[dict]:
    """Convert content sections into ShareGPT-format Q&A pairs."""
    pairs: list[dict] = []
    idx = 0

    # Skip sections that are boilerplate
    skip_patterns = [
        r"^Languages$",
        r"^Welcome$",
        r"^Contents$",
        r"^Introduction$",
    ]

    for section in sections:
        # Check skip patterns
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, section.heading, re.IGNORECASE):
                skip = True
                break
        if skip:
            continue

        body = section.body.strip()
        if len(body) < min_section_chars:
            continue

        # Chunk if too long
        chunks = chunk_text(body, max_chunk_chars, heading=section.heading)

        for chunk in chunks:
            chunk = chunk.strip()
            if len(chunk) < min_section_chars:
                continue

            question = generate_question(section.heading, idx)
            pairs.append({
                "conversations": [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": chunk},
                ]
            })
            idx += 1

    return pairs


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------
def discover_markdown_files(input_dir: str) -> list[Path]:
    """Recursively find all .md files in the input directory."""
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    md_files = sorted(input_path.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in: {input_dir}")

    return md_files


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def build_dataset(
    input_dir: str,
    output_path: str,
    max_chunk_chars: int = 2000,
    min_section_chars: int = 50,
) -> None:
    """Full pipeline: discover → parse → clean → Q&A → JSONL."""

    md_files = discover_markdown_files(input_dir)
    print(f"📂 Found {len(md_files)} markdown file(s) in '{input_dir}':")
    for f in md_files:
        print(f"   • {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    all_pairs: list[dict] = []

    for md_file in md_files:
        print(f"\n📄 Processing: {md_file.name}")
        raw_text = md_file.read_text(encoding="utf-8")

        # Clean PDF artifacts
        cleaned = clean_body(raw_text)

        # Parse into logical content sections
        sections = parse_content_sections(cleaned)
        print(f"   Found {len(sections)} content sections")

        # Show the section headings for debugging
        for s in sections[:10]:
            print(f"     → {s.heading} ({len(s.body)} chars)")
        if len(sections) > 10:
            print(f"     ... and {len(sections) - 10} more")

        # Build Q&A pairs
        pairs = build_qa_pairs(
            sections,
            max_chunk_chars=max_chunk_chars,
            min_section_chars=min_section_chars,
        )
        print(f"   Generated {len(pairs)} Q&A pairs")
        all_pairs.extend(pairs)

    # Write JSONL
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    # Summary statistics
    total_chars = sum(
        len(p["conversations"][1]["content"]) for p in all_pairs
    )
    avg_chars = total_chars // len(all_pairs) if all_pairs else 0

    print(f"\n{'='*60}")
    print(f"✅ Dataset built successfully!")
    print(f"   Output:          {output}")
    print(f"   Total Q&A pairs: {len(all_pairs)}")
    print(f"   Total chars:     {total_chars:,}")
    print(f"   Avg answer len:  {avg_chars:,} chars")
    print(f"{'='*60}")

    # Show samples from different parts of the dataset
    if all_pairs:
        print(f"\n📋 Sample Q&A pairs:")
        samples = [0, len(all_pairs) // 4, len(all_pairs) // 2, 3 * len(all_pairs) // 4]
        for si in samples:
            if si < len(all_pairs):
                sample = all_pairs[si]
                q = sample["conversations"][0]["content"]
                a_preview = sample["conversations"][1]["content"][:150].replace("\n", " ")
                print(f"\n   Q: {q}")
                print(f"   A: {a_preview}...")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to ShareGPT-format JSONL for LLM fine-tuning.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dataset_builder.py
  python dataset_builder.py --input-dir ./Data --output ./Data/training_data.jsonl
  python dataset_builder.py --max-chunk-chars 3000 --min-section-chars 100
        """,
    )
    parser.add_argument(
        "--input-dir",
        default="./Data",
        help="Directory containing .md files to process (default: ./Data)",
    )
    parser.add_argument(
        "--output",
        default="./Data/training_data.jsonl",
        help="Output JSONL file path (default: ./Data/training_data.jsonl)",
    )
    parser.add_argument(
        "--max-chunk-chars",
        type=int,
        default=2000,
        help="Maximum characters per answer chunk (default: 2000)",
    )
    parser.add_argument(
        "--min-section-chars",
        type=int,
        default=50,
        help="Minimum characters for a section to be included (default: 50)",
    )
    args = parser.parse_args()

    build_dataset(
        input_dir=args.input_dir,
        output_path=args.output,
        max_chunk_chars=args.max_chunk_chars,
        min_section_chars=args.min_section_chars,
    )


if __name__ == "__main__":
    main()
