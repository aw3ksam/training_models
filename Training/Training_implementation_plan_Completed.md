# Unsloth LLM Fine-Tuning Pipeline

Build a reproducible, modular pipeline to fine-tune an LLM on the Blackmagic PYXIS camera manual using the Unsloth library.

## User Review Required

> [!IMPORTANT]
> **Base Model Selection**: The reference notebooks demonstrate two paths — **Gemma 3 4B** (newer `FastModel` API) and **Llama 3 8B** (older `FastLanguageModel` API). The training script will default to **Gemma 3 4B** (4-bit quantized via `unsloth/gemma-3-4b-it-unsloth-bnb-4bit`) since it's the more recent notebook pattern and works on a free T4 Colab GPU. However, the script will be parameterized so you can swap to any supported model (Llama 3, Phi-4, Mistral, etc.) via CLI flags. Is Gemma 3 4B acceptable as the default?

> [!IMPORTANT]
> **Dataset Strategy — Q&A Pairs from Manual**: The Blackmagic PYXIS Manual is a ~525KB, ~10,900-line technical document. The Unsloth notebooks expect data in **ShareGPT conversational format** (`[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`). I propose a **section-based Q&A extraction strategy**:
> - Parse the manual into logical sections using markdown heading structure (`##`, `###`, etc.)
> - For each section, generate a Q&A pair where the **user question** is derived from the section heading (e.g., "How do I attach a lens to the Blackmagic PYXIS?" from the "Attaching a Lens" section), and the **assistant response** is the section content.
> - Sections exceeding `max_seq_length` (2048 tokens by default) will be chunked with overlap to prevent data loss.
> - This yields a dataset of several hundred high-quality instructional Q&A pairs. Is this approach acceptable, or would you prefer a different chunking/prompting strategy?

> [!WARNING]
> **GPU Requirement**: Unsloth + 4-bit LoRA fine-tuning requires a CUDA-capable NVIDIA GPU (minimum ~8GB VRAM for Gemma 3 4B). Your Mac M1 Max does **not** have CUDA. The training script will need to run on a machine with an NVIDIA GPU (e.g., Google Colab T4, cloud instance, or a separate Linux box). The `dataset_builder.py` script runs on any machine.

## Open Questions

> [!IMPORTANT]
> 1. **System prompt**: Should the fine-tuned model have a specific system persona? For example: *"You are a Blackmagic PYXIS camera expert. Answer user questions about the camera's features, settings, and operation based on the official manual."* Or do you prefer no system prompt?

> [!NOTE]
> 2. **Additional training data**: Currently only `Data/BlackmagicPYXISManual.md` exists. If more `.md` files are added to `Data/` later, `dataset_builder.py` will automatically discover and process all of them. Should the script support any additional formats beyond `.md`?

---

## Proposed Changes

### Dataset Builder

#### [NEW] [dataset_builder.py](file:///Users/studio/Documents/Sandbox/dataset_builder.py)

A standalone Python script that converts markdown files into a Hugging Face-compatible JSONL training dataset.

**Parsing Logic**:
1. Recursively discover all `.md` files in `./Data/`
2. Parse each file by splitting on markdown headings (`##` and `###`)
3. Skip non-English content (the manual contains translations starting after line ~10922)
4. Extract section title and body text for each section
5. Clean artifacts: remove page markers (`_Pages X–Y_`), excessive whitespace, empty sections
6. Generate Q&A pairs in ShareGPT format:
   ```json
   {
     "conversations": [
       {"role": "user", "content": "Explain how to [section topic] on the Blackmagic PYXIS."},
       {"role": "assistant", "content": "[cleaned section content]"}
     ]
   }
   ```
7. Chunk long sections (>2000 chars) into smaller pieces with contextual headings preserved
8. Output to `./Data/training_data.jsonl`

**Question Generation Templates** (varied to avoid overfitting):
- "How do I {heading}?"
- "Explain {heading} on the Blackmagic PYXIS."
- "What should I know about {heading}?"
- "Describe the process of {heading}."
- "Tell me about {heading} for the Blackmagic PYXIS camera."

**CLI Arguments**:
- `--input-dir` (default: `./Data/`)
- `--output` (default: `./Data/training_data.jsonl`)
- `--max-chunk-chars` (default: `2000`)
- `--min-section-chars` (default: `50`) — skip tiny sections

---

### Training Script

#### [NEW] [train_unsloth.py](file:///Users/studio/Documents/Sandbox/train_unsloth.py)

A modular training script that mirrors the patterns from both the Gemma3 and Llama3 Unsloth notebooks, parameterized for flexibility.

**Pipeline Steps** (matching notebook flow):

1. **Load Model** — `FastModel.from_pretrained()` with configurable:
   - `model_name` (default: `unsloth/gemma-3-4b-it-unsloth-bnb-4bit`)
   - `max_seq_length` (default: `2048`)
   - `load_in_4bit` (default: `True`)

2. **Apply LoRA Adapters** — `FastModel.get_peft_model()` with configurable:
   - `r` (default: `8`)
   - `lora_alpha` (default: `8`)
   - `lora_dropout` (default: `0`)
   - `finetune_vision_layers` = `False` (text-only)
   - `finetune_language_layers` = `True`
   - `finetune_attention_modules` = `True`
   - `finetune_mlp_modules` = `True`

3. **Load & Prepare Dataset**:
   - Load from `training_data.jsonl` using `datasets.load_dataset("json", ...)`
   - Apply chat template using `get_chat_template(tokenizer, chat_template="gemma-3")`
   - Use `standardize_data_formats()` to normalize
   - Format with `apply_chat_template` and store in `"text"` field

4. **Configure SFTTrainer** — from `trl.SFTTrainer` + `SFTConfig`:
   - `per_device_train_batch_size`: `2`
   - `gradient_accumulation_steps`: `4`
   - `warmup_steps`: `5`
   - `num_train_epochs`: `3` (default for small dataset, vs 1 for large datasets)
   - `learning_rate`: `2e-4`
   - `optim`: `adamw_8bit`
   - `weight_decay`: `0.001`
   - `lr_scheduler_type`: `linear`
   - `logging_steps`: `1`
   - `output_dir`: `./outputs`
   - `report_to`: `none`

5. **Train on Completions Only** — `train_on_responses_only()` to mask user instruction loss (from Gemma3 notebook)

6. **Train** — `trainer.train()`

7. **Save**:
   - LoRA adapters: `model.save_pretrained("./lora_model")`
   - Optionally merged 16-bit: `model.save_pretrained_merged()`
   - Optionally GGUF: `model.save_pretrained_gguf()` with Q8_0

**CLI Arguments** (all configurable):
```
--dataset-path       Path to JSONL file (default: ./Data/training_data.jsonl)
--model-name         HuggingFace model ID (default: unsloth/gemma-3-4b-it-unsloth-bnb-4bit)
--max-seq-length     Maximum sequence length (default: 2048)
--epochs             Number of training epochs (default: 3)
--batch-size         Per-device batch size (default: 2)
--learning-rate      Learning rate (default: 2e-4)
--lora-r             LoRA rank (default: 8)
--lora-alpha         LoRA alpha (default: 8)
--output-dir         Checkpoint output directory (default: ./outputs)
--save-dir           Final model save directory (default: ./lora_model)
--save-gguf          Whether to also save GGUF format (flag)
--chat-template      Chat template name (default: gemma-3)
```

---

### Project Documentation

#### [NEW] [CLAUDE.md](file:///Users/studio/Documents/Sandbox/CLAUDE.md)

A comprehensive project instruction file covering:

1. **Project Goal** — Fine-tune an LLM on the Blackmagic PYXIS camera manual using Unsloth for domain-specific Q&A
2. **Directory Structure** — Map of all project directories and files
3. **System Dependencies** — Python ≥3.10, CUDA toolkit, NVIDIA GPU
4. **Python Package Requirements** — `unsloth`, `torch`, `trl`, `transformers`, `datasets`, `peft`, `bitsandbytes`, `accelerate`, `sentencepiece`
5. **Step-by-Step Workflow** — Exact commands for dataset creation → training → export
6. **Hyperparameter Guide** — Table of all tunable parameters with descriptions and recommended ranges
7. **Model Swapping Guide** — How to switch between Gemma 3, Llama 3, Phi-4, Mistral etc.
8. **Troubleshooting** — Common CUDA OOM fixes, dataset issues, version pinning

---

## Verification Plan

### Automated Tests
1. Run `python dataset_builder.py` and verify:
   - `training_data.jsonl` is created
   - Each line is valid JSON with `conversations` key
   - Each conversation has exactly 2 entries (user + assistant)
   - No empty content fields
   - Output line count is reasonable (100-500 Q&A pairs expected)
2. Validate `train_unsloth.py --help` prints all CLI arguments correctly
3. Validate `CLAUDE.md` exists and contains all required sections

### Manual Verification
- The user should transfer `train_unsloth.py` and `training_data.jsonl` to a CUDA-capable machine (e.g., Google Colab) and run the training to verify end-to-end execution
