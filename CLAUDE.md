# CLAUDE.md — Unsloth LLM Fine-Tuning Pipeline

## Project Goal

Fine-tune an LLM on the **Blackmagic PYXIS camera manual** using the [Unsloth](https://github.com/unslothai/unsloth) library to create a domain-specific Q&A assistant. The pipeline converts PDF-derived Markdown documentation into a structured training dataset, then uses Unsloth's optimized LoRA fine-tuning to train a conversational model.

---

## Directory Structure

```
.
├── CLAUDE.md                    # This file — project instructions
├── dataset_builder.py           # Markdown → JSONL dataset builder
├── train_unsloth.py             # Unsloth fine-tuning script (TODO)
├── Data/
│   ├── BlackmagicPYXISManual.md # Source training data (Markdown from PDF)
│   └── training_data.jsonl      # Generated training dataset (ShareGPT format)
├── Creating Database/           # Reference documentation
│   ├── Gemma3_(4B).ipynb        # Unsloth Gemma 3 training notebook (reference)
│   ├── Llama3_(8B)_Ollama.ipynb # Unsloth Llama 3 training notebook (reference)
│   ├── Creating Datasets with Hugging Face.md
│   ├── Accessing Datasets_ Dataset vs. IterableDataset.md
│   ├── Datasets Preprocessing for Machine Learning.md
│   └── Hugging Face Datasets Processing Guide.md
├── OtherFormats/
│   ├── BlackmagicPYXISManual.pdf # Original PDF manual
│   └── TableOfContents.md       # Extracted table of contents
├── Training/                    # Training outputs (created during training)
├── outputs/                     # Checkpoints (created during training)
└── lora_model/                  # Final LoRA adapters (created during training)
```

---

## System Dependencies

| Dependency | Version | Notes |
|---|---|---|
| Python | ≥ 3.10 | Required for type hints |
| CUDA Toolkit | ≥ 12.1 | **NVIDIA GPU required for training** |
| NVIDIA GPU | ≥ 8GB VRAM | T4 (free Colab), A100, RTX 3060+ |

> **Note**: `dataset_builder.py` runs on **any machine** (Mac, Linux, Windows) — no GPU needed.
> Training with `train_unsloth.py` requires a CUDA-capable NVIDIA GPU.

---

## Python Package Requirements

Install all dependencies:

```bash
pip install unsloth
pip install transformers==4.56.2
pip install --no-deps trl==0.22.2
pip install torch datasets peft bitsandbytes accelerate sentencepiece protobuf
```

For Google Colab (auto-detects CUDA version):

```python
import os, re, torch
v = re.match(r'[\d]{1,}\.[\d]{1,}', str(torch.__version__)).group(0)
xformers = 'xformers==' + {'2.10':'0.0.34','2.9':'0.0.33.post1','2.8':'0.0.32.post2'}.get(v, "0.0.34")
!pip install sentencepiece protobuf "datasets==4.3.0" "huggingface_hub>=0.34.0" hf_transfer
!pip install --no-deps unsloth_zoo bitsandbytes accelerate {xformers} peft trl triton unsloth
!pip install transformers==4.56.2
!pip install --no-deps trl==0.22.2
```

### Core Package Roles

| Package | Purpose |
|---|---|
| `unsloth` | Optimized LoRA fine-tuning (2x faster, 60% less VRAM) |
| `torch` | PyTorch backend for model inference and training |
| `trl` | Supervised Fine-Tuning Trainer (SFTTrainer) |
| `transformers` | Hugging Face model loading, tokenizers, generation |
| `datasets` | Hugging Face dataset loading and processing |
| `peft` | Parameter-Efficient Fine-Tuning (LoRA adapters) |
| `bitsandbytes` | 4-bit/8-bit quantization |
| `accelerate` | Distributed training utilities |

---

## Step-by-Step Workflow

### Step 1: Build the Training Dataset

```bash
# From the project root directory
python dataset_builder.py
```

This parses `Data/BlackmagicPYXISManual.md` and generates `Data/training_data.jsonl`.

**What it does:**
1. Discovers all `.md` files in `Data/`
2. Parses sections based on inline title-cased headings
3. Skips table-of-contents regions and PDF artifacts
4. Generates varied Q&A pairs in ShareGPT conversational format
5. Chunks long sections to stay within model context limits
6. Outputs JSONL with `{"conversations": [{"role": "user", ...}, {"role": "assistant", ...}]}`

**CLI Options:**
```bash
python dataset_builder.py --input-dir ./Data \
                          --output ./Data/training_data.jsonl \
                          --max-chunk-chars 2000 \
                          --min-section-chars 50
```

### Step 2: Transfer to GPU Machine

Copy these files to your training machine (Colab, cloud VM, etc.):
- `Data/training_data.jsonl`
- `train_unsloth.py`

### Step 3: Run Training

```bash
python train_unsloth.py --dataset-path ./Data/training_data.jsonl
```

**Key training CLI flags:**
```bash
python train_unsloth.py \
    --dataset-path ./Data/training_data.jsonl \
    --model-name unsloth/gemma-3-4b-it-unsloth-bnb-4bit \
    --max-seq-length 2048 \
    --epochs 3 \
    --batch-size 2 \
    --learning-rate 2e-4 \
    --lora-r 8 \
    --output-dir ./outputs \
    --save-dir ./lora_model
```

### Step 4: Export Model

After training, the LoRA adapters are saved to `./lora_model`. To export:

```python
# Merged 16-bit (for vLLM deployment)
model.save_pretrained_merged("model-finetune", tokenizer)

# GGUF (for Ollama / llama.cpp)
model.save_pretrained_gguf("model-finetune-gguf", tokenizer, quantization_method="Q8_0")
```

---

## Hyperparameter Guide

| Parameter | Default | Description | Recommended Range |
|---|---|---|---|
| `max_seq_length` | 2048 | Max tokens per training example | 1024–8192 |
| `load_in_4bit` | True | 4-bit quantization (saves VRAM) | True for ≤16GB VRAM |
| `r` (LoRA rank) | 8 | LoRA adapter rank — higher = more capacity | 4, 8, 16, 32, 64 |
| `lora_alpha` | 8 | LoRA scaling factor (set ≥ r) | Same as `r` |
| `lora_dropout` | 0 | Dropout on LoRA layers (0 is optimized) | 0 or 0.05 |
| `per_device_train_batch_size` | 2 | Batch size per GPU | 1–8 (limited by VRAM) |
| `gradient_accumulation_steps` | 4 | Effective batch = batch_size × this | 2–16 |
| `learning_rate` | 2e-4 | Initial learning rate | 1e-5 to 5e-4 |
| `num_train_epochs` | 3 | Training epochs (3 for small datasets) | 1–5 |
| `warmup_steps` | 5 | LR warmup steps | 5–50 |
| `weight_decay` | 0.001 | L2 regularization | 0.001–0.01 |
| `lr_scheduler_type` | linear | Learning rate decay schedule | linear, cosine |
| `optim` | adamw_8bit | Optimizer (8-bit saves VRAM) | adamw_8bit, adamw_torch |

### Rules of Thumb

- **Small dataset (<1K examples)**: Use `epochs=3-5`, `lr=2e-4`, `r=8`
- **Medium dataset (1K-10K examples)**: Use `epochs=1-2`, `lr=2e-4`, `r=16`
- **Large dataset (>10K examples)**: Use `epochs=1`, `lr=2e-5`, `r=16-32`
- **If overfitting**: Reduce `r`, reduce `epochs`, increase `weight_decay`
- **If underfitting**: Increase `r`, increase `epochs`, increase `learning_rate`
- **OOM errors**: Reduce `batch_size` to 1, increase `gradient_accumulation_steps`

---

## How to Swap Base Models

The training script supports any Unsloth-compatible model. Change the `--model-name` flag:

### Recommended Models

| Model | HuggingFace ID | VRAM Needed | Notes |
|---|---|---|---|
| **Gemma 3 4B** (default) | `unsloth/gemma-3-4b-it-unsloth-bnb-4bit` | ~8GB | Best for T4 Colab |
| Gemma 3 12B | `unsloth/gemma-3-12b-it-unsloth-bnb-4bit` | ~12GB | Better quality |
| Gemma 3 27B | `unsloth/gemma-3-27b-it-unsloth-bnb-4bit` | ~20GB | Highest quality |
| Llama 3.1 8B | `unsloth/Llama-3.1-8B` | ~8GB | Strong all-rounder |
| Llama 3.3 70B | `unsloth/Llama-3.3-70B` | ~40GB | Needs A100 |
| Mistral 7B | `unsloth/mistral-7b-instruct-v0.3` | ~8GB | Fast inference |
| Phi-4 | `unsloth/Phi-4` | ~8GB | Microsoft's small model |

### Important Notes When Swapping Models

1. **Chat template must match the model**:
   - Gemma 3: `--chat-template gemma-3`
   - Llama 3: `--chat-template llama-3`
   - Mistral: `--chat-template mistral`
   - General: `--chat-template chatml`

2. **Newer models use `FastModel`**, older models use `FastLanguageModel`:
   - The training script handles this automatically based on model name

3. **Instruction-tuned models** (names ending in `-it` or `-instruct`) work best for Q&A fine-tuning

---

## Dataset Format Reference

The training dataset (`training_data.jsonl`) uses **ShareGPT conversational format**:

```json
{
  "conversations": [
    {"role": "user", "content": "How do I attach a lens on the Blackmagic PYXIS?"},
    {"role": "assistant", "content": "To attach a lens to your camera, begin by removing the protective dust cap..."}
  ]
}
```

Each line is a self-contained JSON object with exactly one user-assistant turn.

### Adding New Training Data

1. Place new `.md` files in the `Data/` directory
2. Re-run `python dataset_builder.py`
3. The script automatically discovers and processes all `.md` files

---

## Troubleshooting

### CUDA Out of Memory
```
RuntimeError: CUDA out of memory
```
- Reduce `--batch-size` to 1
- Increase `--gradient-accumulation-steps` to 8
- Set `load_in_4bit = True`
- Reduce `--max-seq-length` to 1024

### Version Conflicts
Pin these exact versions for compatibility:
```bash
pip install transformers==4.56.2
pip install --no-deps trl==0.22.2
```

### Empty Dataset
If `dataset_builder.py` produces 0 pairs:
- Check that `.md` files exist in `--input-dir`
- Try reducing `--min-section-chars` to 30
- Ensure the markdown has proper heading structure

### Training Loss Not Decreasing
- Verify the dataset is loaded correctly (check `trainer.train_dataset[0]`)
- Try increasing `--learning-rate` to 5e-4
- Increase `--epochs` for small datasets
- Check that `train_on_responses_only` is applied correctly
