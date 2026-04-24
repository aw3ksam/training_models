# Markdown to Dataset Converter

This repository contains tools to convert markdown files into dataset formats suitable for LLM fine-tuning (e.g., Unsloth formats like ShareGPT or Alpaca). You can perform this conversion using either a web interface or the command line.

## Prerequisites

To run these tools, you will need the following installed:
- Python 3.x
- Flask (required for the Web UI)

### Mac Users
If you are on a Mac, you can install Python and Flask using [Homebrew](https://brew.sh/):
```bash
brew install python
pip3 install flask
```

### Linux Users
If you are on Linux, ensure Python 3 is installed, then install Flask using pip:
```bash
pip install flask
```

## How to use the Web UI

The web interface is the easiest way to convert your markdown files into a dataset. 

1. Start the web application by running:
   ```bash
   python web_app.py
   ```
2. Open your browser and navigate to the standard port used by the UI:
   **http://localhost:6756**
3. Drag and drop your `.md` files into the designated area on the page.
4. Fill out the "Topic" field and select your preferred dataset format (ShareGPT or Alpaca).
5. Click the "Convert" button. Once processing is complete, you can download the generated `.jsonl` file directly.

## How to use the CLI

If you prefer to use the terminal, you can use the command-line interfaces provided.

### Using `convert_cli.py`

This script provides an easy way to process specific files or directories:

```bash
# Convert all .md files in the default 'input' folder
python convert_cli.py

# Convert specific markdown files
python convert_cli.py --files doc1.md path/to/doc2.md

# Combine a directory scan with extra files
python convert_cli.py --input-dir ./manuals --files extra_notes.md

# Customize output format, topic, and max chunk characters
python convert_cli.py --fmt alpaca --topic "camera manual" --max-chunk 3000
```

### Using `md_to_dataset.py`

You can also use the core converter directly:

```bash
# Process files in the default input folder
python md_to_dataset.py

# Specify input directory and output file
python md_to_dataset.py --input-dir ./Data --output ./Data/training_data.jsonl

# Specify topic and format
python md_to_dataset.py --topic "my product manual" --format alpaca
```
