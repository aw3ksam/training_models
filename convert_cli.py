#!/usr/bin/env python3
"""
convert_cli.py — Convert markdown files to an Unsloth dataset without the web app.

Examples:
  # Convert all .md files in the default 'input' folder:
  python convert_cli.py

  # Combine specific files from anywhere into one dataset:
  python convert_cli.py --files doc1.md path/to/doc2.md another/doc3.md

  # Mix a directory scan with extra files:
  python convert_cli.py --input-dir ./manuals --files extra_notes.md

  # Customise output format and topic:
  python convert_cli.py --fmt alpaca --topic "camera manual" --max-chunk 3000
"""

import argparse
from pathlib import Path
from md_to_dataset import build_dataset, discover_markdown_files


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown files to an Unsloth training dataset.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="input",
        help="Directory containing .md files (default: 'input'). "
             "Ignored when --files is used alone.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        metavar="FILE",
        help="One or more .md file paths to include. "
             "Can be combined with --input-dir to add extras.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="output/training_data.jsonl",
        help="Output JSONL file path (default: 'output/training_data.jsonl').",
    )
    parser.add_argument(
        "--max-chunk",
        type=int,
        default=2000,
        help="Max characters per answer chunk (default: 2000).",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="this document",
        help="Topic label used in generated questions (default: 'this document').",
    )
    parser.add_argument(
        "--fmt",
        type=str,
        choices=["sharegpt", "alpaca"],
        default="sharegpt",
        help="Output format (default: 'sharegpt').",
    )

    args = parser.parse_args()

    # ---- Resolve the list of markdown files ----
    md_files: list[Path] = []

    input_dir = Path(args.input_dir)
    use_dir = args.files is None or input_dir.exists()

    # Collect from directory (unless only --files was given with no valid dir)
    if use_dir and input_dir.is_dir():
        dir_files = sorted(input_dir.rglob("*.md"))
        md_files.extend(dir_files)

    # Collect explicit --files
    if args.files:
        for fp in args.files:
            p = Path(fp)
            if not p.exists():
                print(f"Warning: File '{fp}' not found, skipping.")
                continue
            if not p.suffix == ".md":
                print(f"Warning: '{fp}' is not a .md file, skipping.")
                continue
            if p not in md_files:
                md_files.append(p)

    if not md_files:
        print("Error: No markdown files found. Provide --input-dir and/or --files.")
        return

    # Deduplicate (resolve to absolute to catch path duplicates)
    seen = set()
    unique: list[Path] = []
    for f in md_files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    md_files = unique

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Combining {len(md_files)} markdown file(s) into '{output_path}'")
    print(f"Settings: format={args.fmt}, topic='{args.topic}', max_chunk={args.max_chunk}")
    print()

    try:
        result = build_dataset(
            output_path=str(output_path),
            max_chunk_chars=args.max_chunk,
            min_section_chars=50,
            topic=args.topic,
            fmt=args.fmt,
            md_files=md_files,
        )
        print(f"\nDone! Generated {result['pairs']} Q&A pairs → {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")


if __name__ == "__main__":
    main()
