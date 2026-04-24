#!/usr/bin/env python3
"""
web_app.py — Minimal web UI for md_to_dataset.py

Run:  python web_app.py
Open: http://localhost:5000
"""

import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from flask import Flask, request, send_file, render_template_string

from md_to_dataset import build_dataset

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MD → Unsloth Dataset</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: system-ui, sans-serif;
    background: #0f0f0f;
    color: #e5e5e5;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 2.5rem;
    width: 100%;
    max-width: 540px;
  }
  h1 { font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem; color: #fff; }
  .field { margin-bottom: 1.25rem; }
  label { display: block; font-size: 0.8rem; color: #888; margin-bottom: 0.4rem; letter-spacing: 0.04em; text-transform: uppercase; }
  input[type=text], input[type=number], select {
    width: 100%;
    background: #111;
    border: 1px solid #333;
    border-radius: 6px;
    color: #e5e5e5;
    font-size: 0.95rem;
    padding: 0.55rem 0.75rem;
    outline: none;
  }
  input:focus, select:focus { border-color: #555; }
  .drop-zone {
    border: 2px dashed #333;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    color: #666;
    font-size: 0.9rem;
  }
  .drop-zone.over { border-color: #4f8ef7; background: #111c2e; color: #aac8ff; }
  .drop-zone.has-files { border-color: #2d8a4e; color: #6fcf97; }
  .drop-zone input[type=file] { display: none; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  button {
    width: 100%;
    background: #4f8ef7;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    padding: 0.7rem;
    cursor: pointer;
    margin-top: 0.5rem;
    transition: background 0.2s;
  }
  button:hover:not(:disabled) { background: #3a7be0; }
  button:disabled { background: #2a3a5a; color: #556; cursor: default; }
  #status {
    margin-top: 1.25rem;
    font-size: 0.85rem;
    color: #888;
    min-height: 1.2em;
  }
  #status.err { color: #f87171; }
  #status.ok  { color: #6fcf97; }
  #dl-link {
    display: none;
    margin-top: 1rem;
    background: #1e3a1e;
    border: 1px solid #2d8a4e;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    color: #6fcf97;
    text-decoration: none;
    text-align: center;
  }
  #dl-link:hover { background: #243f24; }
</style>
</head>
<body>
<div class="card">
  <h1>Markdown → Unsloth Dataset</h1>

  <div class="field">
    <label>Markdown Files</label>
    <div class="drop-zone" id="drop" onclick="document.getElementById('file-input').click()">
      Drop .md files here or click to browse
      <input type="file" id="file-input" multiple accept=".md">
    </div>
  </div>

  <div class="field">
    <label>Topic</label>
    <input type="text" id="topic" placeholder="e.g. camera manual, Python guide" value="this document">
  </div>

  <div class="row">
    <div class="field">
      <label>Format</label>
      <select id="fmt">
        <option value="sharegpt">ShareGPT (Llama / Gemma / GPT)</option>
        <option value="alpaca">Alpaca</option>
      </select>
    </div>
    <div class="field">
      <label>Max Chunk Chars</label>
      <input type="number" id="max-chunk" value="2000" min="200" max="8000" step="100">
    </div>
  </div>

  <button id="btn" onclick="convert()">Convert</button>
  <div id="status"></div>
  <a id="dl-link" href="#">⬇ Download dataset</a>
</div>

<script>
const drop = document.getElementById('drop');
const fileInput = document.getElementById('file-input');

fileInput.addEventListener('change', () => updateDrop(fileInput.files));
drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('over'); });
drop.addEventListener('dragleave', () => drop.classList.remove('over'));
drop.addEventListener('drop', e => {
  e.preventDefault();
  drop.classList.remove('over');
  fileInput.files = e.dataTransfer.files;
  updateDrop(fileInput.files);
});

function updateDrop(files) {
  const mdFiles = [...files].filter(f => f.name.endsWith('.md'));
  drop.classList.toggle('has-files', mdFiles.length > 0);
  drop.textContent = mdFiles.length > 0
    ? mdFiles.length + ' file' + (mdFiles.length > 1 ? 's' : '') + ' selected: ' + mdFiles.map(f => f.name).join(', ')
    : 'Drop .md files here or click to browse';
  if (mdFiles.length > 0) {
    const hidden = document.createElement('input');
    hidden.type = 'file'; hidden.id = 'file-input'; hidden.multiple = true; hidden.accept = '.md';
    hidden.style.display = 'none';
    drop.appendChild(hidden);
  }
}

async function convert() {
  const files = fileInput.files;
  if (!files.length) { setStatus('Select at least one .md file.', 'err'); return; }

  const btn = document.getElementById('btn');
  const dlLink = document.getElementById('dl-link');
  btn.disabled = true;
  dlLink.style.display = 'none';
  setStatus('Converting...');

  const fd = new FormData();
  for (const f of files) fd.append('files', f);
  fd.append('topic', document.getElementById('topic').value || 'this document');
  fd.append('fmt', document.getElementById('fmt').value);
  fd.append('max_chunk', document.getElementById('max-chunk').value);

  try {
    const res = await fetch('/convert', { method: 'POST', body: fd });
    if (!res.ok) {
      const err = await res.text();
      setStatus('Error: ' + err, 'err');
    } else {
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const filename = res.headers.get('X-Filename') || 'training_data.jsonl';
      dlLink.href = url;
      dlLink.download = filename;
      dlLink.textContent = '⬇ Download ' + filename;
      dlLink.style.display = 'block';
      const pairs = res.headers.get('X-Pairs') || '?';
      setStatus('Done — ' + pairs + ' Q&A pairs generated.', 'ok');
    }
  } catch (e) {
    setStatus('Request failed: ' + e.message, 'err');
  } finally {
    btn.disabled = false;
  }
}

function setStatus(msg, cls) {
  const el = document.getElementById('status');
  el.textContent = msg;
  el.className = cls || '';
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("files")
    if not files:
        return "No files uploaded.", 400

    topic = request.form.get("topic", "this document").strip() or "this document"
    fmt = request.form.get("fmt", "sharegpt")
    if fmt not in ("sharegpt", "alpaca"):
        fmt = "sharegpt"

    try:
        max_chunk = int(request.form.get("max_chunk", 2000))
    except ValueError:
        max_chunk = 2000

    # Clear old input files, write new ones
    for old in INPUT_DIR.glob("*.md"):
        old.unlink()

    for f in files:
        if f.filename and f.filename.endswith(".md"):
            safe_name = Path(f.filename).name
            f.save(INPUT_DIR / safe_name)

    md_files = list(INPUT_DIR.glob("*.md"))
    if not md_files:
        return "No .md files received.", 400

    # Build a unique filename: topic_YYYY-MM-DD_HH-MM-SS.jsonl
    safe_topic = re.sub(r"[^\w]+", "_", topic).strip("_") or "dataset"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_filename = f"{safe_topic}_{timestamp}.jsonl"
    output_path = OUTPUT_DIR / out_filename

    try:
        result = build_dataset(
            input_dir=str(INPUT_DIR),
            output_path=str(output_path),
            max_chunk_chars=max_chunk,
            min_section_chars=50,
            topic=topic,
            fmt=fmt,
        )
    except Exception as e:
        return f"Build failed: {e}", 500

    response = send_file(
        str(output_path),
        as_attachment=True,
        download_name=out_filename,
        mimetype="application/x-ndjson",
    )
    response.headers["X-Pairs"] = str(result["pairs"])
    response.headers["X-Filename"] = out_filename
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6756))
    print(f"Open http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
