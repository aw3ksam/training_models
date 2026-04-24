#!/usr/bin/env python3
"""Markdown → JSONL dataset builder for Unsloth LLM fine-tuning. Generic, reusable."""

import argparse
import json
import re
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# Question templates — {topic} = heading-derived phrase, {subject} = --topic arg
# ---------------------------------------------------------------------------
QUESTION_TEMPLATES = [
    "How do I {topic}?",
    "What is {topic}?",
    "Explain {topic}.",
    "Describe {topic} in detail.",
    "What should I know about {topic}?",
    "Can you explain how {topic} works?",
    "Give me an overview of {topic}.",
    "Walk me through {topic} in {subject}.",
    "How does {topic} work in {subject}?",
    "What are the details of {topic} in {subject}?",
]

random.seed(42)

# ---------------------------------------------------------------------------
# Cleaning helpers
# ---------------------------------------------------------------------------
def clean_body(text: str) -> str:
    """Remove PDF conversion artifacts and normalize whitespace."""
    text = re.sub(r"_Pages?\s*\d+[\s–\-]+\d+_", "", text)
    text = re.sub(
        r"\n[A-Z][A-Za-z &\-'()]+ \d{1,4}\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"\n-{3,}\n", "\n", text)
    text = re.sub(r"\n##\s+[^\n]+\n", "\n", text)
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_toc_line(line: str) -> bool:
    """Return True if the line looks like a table-of-contents entry."""
    stripped = line.strip()
    if re.match(r"^[A-Z][A-Za-z &\-'/()\.]+ \d{1,4}$", stripped):
        return True
    return False


HEADING_BLACKLIST = {
    "Name Type Description",
    "Response",
    "Parameters",
    "Example",
    "Notes",
    "See Also",
}


def is_api_endpoint(line: str) -> bool:
    """Return True if the line is a REST API endpoint definition."""
    return bool(re.match(r"^(GET|PUT|POST|DELETE|PATCH)\s+/", line.strip()))


def is_section_heading(line: str, next_line: str = "") -> bool:
    """Return True if line is a section heading in PDF-converted markdown."""
    stripped = line.strip()

    if not stripped or len(stripped) > 80 or len(stripped) < 3:
        return False

    if stripped in HEADING_BLACKLIST:
        return False

    if is_api_endpoint(stripped):
        return True

    if not stripped[0].isupper():
        return False

    if stripped.endswith((".", ",", ":", ";", "!")):
        return False

    if re.match(r"^\d+\s", stripped):
        return False

    if stripped.startswith(("*", "-", ">", "|", "TIP ", "NOTE ", "http", "www", "©")):
        return False

    if stripped.isupper() and len(stripped) > 20:
        return False

    words = stripped.split()
    if len(words) < 1 or len(words) > 12:
        return False

    if not words[0][0].isupper():
        return False

    title_pattern = re.match(
        r"^[A-Z][A-Za-z0-9]*(?:\s+(?:[a-z]{1,4}|[A-Z/][A-Za-z0-9\-/.'&()]*|[0-9]+[A-Za-z]*))*$",
        stripped,
    )
    if not title_pattern:
        return False

    if is_toc_line(stripped):
        return False

    return True


# ---------------------------------------------------------------------------
# Content section parser
# ---------------------------------------------------------------------------
class ContentSection:
    """A logical section with a heading and body text."""

    def __init__(self, heading: str, body: str):
        self.heading = heading
        self.body = body

    def __repr__(self):
        return f"ContentSection({self.heading!r}, body_len={len(self.body)})"


def identify_toc_region(lines: list[str]) -> tuple[int, int]:
    """Return (start, end) line indices of the table-of-contents region."""
    toc_start = -1
    toc_end = -1
    consecutive_toc = 0
    candidate_start = 0

    for i, line in enumerate(lines):
        if is_toc_line(line.strip()):
            if consecutive_toc == 0:
                candidate_start = i
            consecutive_toc += 1
            if consecutive_toc >= 5:
                if toc_start == -1:
                    toc_start = candidate_start
                toc_end = i
        else:
            if line.strip():
                consecutive_toc = 0

    return toc_start, toc_end


def parse_content_sections(text: str) -> list[ContentSection]:
    """Parse cleaned document text into ContentSection objects."""
    lines = text.splitlines()
    toc_start, toc_end = identify_toc_region(lines)

    sections: list[ContentSection] = []
    current_heading = "Introduction"
    current_body_lines: list[str] = []

    for i, line in enumerate(lines):
        if toc_start <= i <= toc_end:
            continue

        stripped = line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        if is_section_heading(stripped, next_line):
            body = "\n".join(current_body_lines).strip()
            if body and len(body) >= 30:
                sections.append(ContentSection(current_heading, body))
            current_heading = stripped
            current_body_lines = []
        else:
            if is_toc_line(stripped) and not current_body_lines:
                continue
            current_body_lines.append(line)

    body = "\n".join(current_body_lines).strip()
    if body and len(body) >= 30:
        sections.append(ContentSection(current_heading, body))

    return sections


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def chunk_text(text: str, max_chars: int, heading: str = "") -> list[str]:
    """Split text into chunks on paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"\n\n+", text)
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

    if heading and len(chunks) > 1:
        for i in range(1, len(chunks)):
            chunks[i] = f"(Continued - {heading})\n\n{chunks[i]}"

    return chunks


# ---------------------------------------------------------------------------
# Question generation
# ---------------------------------------------------------------------------
# Proper nouns and acronyms that should not be lowercased
SKIP_LOWER = {
    "API", "REST", "XML", "JSON", "HTML", "CSS", "SQL", "HTTP", "HTTPS",
    "URL", "PDF", "USB", "USB-C", "HDMI", "SDK", "CLI", "GPU", "CPU",
    "RAM", "SSD", "iOS", "macOS", "Mac", "Windows", "Linux", "GitHub",
    "OAuth", "ID", "Bluetooth", "WiFi", "HDR", "LoRA",
}


def heading_to_topic(heading: str) -> str:
    """Convert a section heading to a natural-language topic phrase."""
    topic = heading.strip()
    words = topic.split()
    if words and words[0] not in SKIP_LOWER:
        words[0] = words[0][0].lower() + words[0][1:]
    return " ".join(words)


def generate_question(heading: str, idx: int, subject: str = "this document") -> str:
    """Pick a question template deterministically based on index."""
    topic = heading_to_topic(heading)
    template = QUESTION_TEMPLATES[idx % len(QUESTION_TEMPLATES)]
    return template.format(topic=topic, subject=subject)


# ---------------------------------------------------------------------------
# Format helpers
# ---------------------------------------------------------------------------
def make_sharegpt_pair(question: str, answer: str) -> dict:
    """Return a ShareGPT-format record."""
    return {
        "conversations": [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }


def make_alpaca_pair(question: str, answer: str) -> dict:
    """Return an Alpaca-format record."""
    return {"instruction": question, "input": "", "output": answer}


def make_pair(question: str, answer: str, fmt: str) -> dict:
    """Dispatch to the correct format serializer."""
    if fmt == "alpaca":
        return make_alpaca_pair(question, answer)
    if fmt == "sharegpt":
        return make_sharegpt_pair(question, answer)
    raise ValueError(f"Unknown format: {fmt!r}. Expected 'sharegpt' or 'alpaca'.")


# ---------------------------------------------------------------------------
# Q&A pair builder
# ---------------------------------------------------------------------------
SKIP_PATTERNS = [
    r"^Languages$",
    r"^Welcome$",
    r"^Contents$",
    r"^Introduction$",
]


def build_qa_pairs(
    sections: list[ContentSection],
    max_chunk_chars: int = 2000,
    min_section_chars: int = 50,
    subject: str = "this document",
    fmt: str = "sharegpt",
) -> list[dict]:
    """Convert content sections into format-specific Q&A pairs."""
    pairs: list[dict] = []
    idx = 0

    for section in sections:
        if any(re.match(p, section.heading, re.IGNORECASE) for p in SKIP_PATTERNS):
            continue

        body = section.body.strip()
        if len(body) < min_section_chars:
            continue

        chunks = chunk_text(body, max_chunk_chars, heading=section.heading)

        for chunk in chunks:
            chunk = chunk.strip()
            if len(chunk) < min_section_chars:
                continue
            question = generate_question(section.heading, idx, subject=subject)
            pairs.append(make_pair(question, chunk, fmt))
            idx += 1

    return pairs


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------
def discover_markdown_files(input_dir: str) -> list[Path]:
    """Recursively find all .md files in input_dir."""
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    md_files = sorted(input_path.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in: {input_dir}")
    return md_files


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def build_dataset(
    input_dir: str = "",
    output_path: str = "./output/training_data.jsonl",
    max_chunk_chars: int = 2000,
    min_section_chars: int = 50,
    topic: str = "this document",
    fmt: str = "sharegpt",
    md_files: list[Path] | None = None,
) -> dict:
    """Full pipeline: discover -> parse -> clean -> Q&A -> JSONL. Returns summary dict.

    If *md_files* is provided, those files are used directly (input_dir is ignored).
    Otherwise, all .md files under *input_dir* are discovered automatically.
    """
    if fmt not in ("sharegpt", "alpaca"):
        raise ValueError(f"Unknown format: {fmt!r}. Expected 'sharegpt' or 'alpaca'.")

    if md_files is None:
        md_files = discover_markdown_files(input_dir)
        print(f"Found {len(md_files)} markdown file(s) in '{input_dir}':")
    else:
        md_files = [Path(f) for f in md_files]
        print(f"Combining {len(md_files)} markdown file(s):")
    for f in md_files:
        print(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    all_pairs: list[dict] = []

    for md_file in md_files:
        print(f"\nProcessing: {md_file.name}")
        raw_text = md_file.read_text(encoding="utf-8")
        cleaned = clean_body(raw_text)
        sections = parse_content_sections(cleaned)
        print(f"  Found {len(sections)} content sections")
        for s in sections[:10]:
            print(f"    -> {s.heading} ({len(s.body)} chars)")
        if len(sections) > 10:
            print(f"    ... and {len(sections) - 10} more")

        pairs = build_qa_pairs(
            sections,
            max_chunk_chars=max_chunk_chars,
            min_section_chars=min_section_chars,
            subject=topic,
            fmt=fmt,
        )
        print(f"  Generated {len(pairs)} Q&A pairs")
        all_pairs.extend(pairs)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    total_chars = sum(
        len(p["conversations"][1]["content"]) if fmt == "sharegpt" else len(p["output"])
        for p in all_pairs
    )
    avg_chars = total_chars // len(all_pairs) if all_pairs else 0

    print(f"\n{'=' * 60}")
    print(f"Dataset built successfully.")
    print(f"  Output:          {output}")
    print(f"  Format:          {fmt}")
    print(f"  Total Q&A pairs: {len(all_pairs)}")
    print(f"  Total chars:     {total_chars:,}")
    print(f"  Avg answer len:  {avg_chars:,} chars")
    print(f"{'=' * 60}")

    if all_pairs:
        print("\nSample Q&A pairs:")
        samples = [0, len(all_pairs) // 4, len(all_pairs) // 2, 3 * len(all_pairs) // 4]
        for si in samples:
            if si < len(all_pairs):
                pair = all_pairs[si]
                if fmt == "sharegpt":
                    q = pair["conversations"][0]["content"]
                    a_preview = pair["conversations"][1]["content"][:150].replace("\n", " ")
                else:
                    q = pair["instruction"]
                    a_preview = pair["output"][:150].replace("\n", " ")
                print(f"\n  Q: {q}")
                print(f"  A: {a_preview}...")

    return {"pairs": len(all_pairs), "output": str(output), "chars": total_chars}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to JSONL for Unsloth LLM fine-tuning.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md_to_dataset.py
  python md_to_dataset.py --input-dir ./Data --output ./Data/training_data.jsonl
  python md_to_dataset.py --topic "my product manual" --format alpaca
  python md_to_dataset.py --max-chunk-chars 3000 --min-section-chars 100
        """,
    )
    parser.add_argument(
        "--input-dir",
        default="./input",
        help="Directory containing .md files to process (default: ./input)",
    )
    parser.add_argument(
        "--output",
        default="./output/training_data.jsonl",
        help="Output JSONL file path (default: ./output/training_data.jsonl)",
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
    parser.add_argument(
        "--topic",
        default="this document",
        help="Document subject used in question templates (default: 'this document')",
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["sharegpt", "alpaca"],
        default="sharegpt",
        help="Output format: sharegpt or alpaca (default: sharegpt)",
    )
    args = parser.parse_args()

    build_dataset(
        input_dir=args.input_dir,
        output_path=args.output,
        max_chunk_chars=args.max_chunk_chars,
        min_section_chars=args.min_section_chars,
        topic=args.topic,
        fmt=args.fmt,
    )


if __name__ == "__main__":
    main()
