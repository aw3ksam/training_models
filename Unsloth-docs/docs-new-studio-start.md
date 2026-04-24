---
source_url: "https://unsloth.ai/docs/new/studio/start"
title: "Get started with Unsloth Studio"
converted_at: "2026-04-22T05:11:13.112452"
---

# Get started Unsloth Studio

Unsloth Studio local, browser-based GUI fine-tuning LLMs without writing code. wraps training pipeline clean interface handles model loading, dataset formatting, hyperparameter configuration, live training monitoring.

<a href="#studio-quickstart" class="button secondary" data-icon="bolt">Studio</a><a href="#data-recipes-quickstart" class="button secondary" data-icon="hat-chef">Data Recipe</a><a href="#export-quickstart" class="button secondary" data-icon="box-isometric">Export</a><a href="#chat-quickstart" class="button secondary" data-icon="comment-dots">Chat</a><a href="#video-tutorial" class="button secondary" data-icon="video">Video</a>

#### Setup Unsloth Studio

First, launch Unsloth Studio using either local install cloud option. Follow [install instructions](https://unsloth.ai/docs/new/studio/install) setup, use [free Colab](https://unsloth.ai/docs/new/studio/..#google-colab-notebook) notebook. local setup, run:

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

open `http://localhost:8888` browser.

{% columns %}
{% column %}
first launch will need create password secure account sign later.

’ll see brief onboarding wizard choose model, dataset, basic settings. can skip time configure everything manually.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZPtRrwafzmVX54HhyyBD%2FScreenshot%202026-03-16%20at%2011.25.22%E2%80%AFPM.png?alt=media&#x26;token=9153c153-ec61-4fff-b1b9-db7f70ac2936" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

## <i class="fa-bolt">:bolt:</i> Studio - Quickstart

Unsloth Studio homepage 4 main areas: [Model](#id-1.-select-model-and-method), [Dataset](#id-2.-dataset), [Parameters](#id-3.-hyperparameters), [Training/Config](#id-4.-training-and-config)

* **Easy setup models data** Hugging Face local files
* **Flexible training choices** QLoRA, LoRA, full fine-tuning, defaults filled 
* **Helpful config tools** splits, column mapping, hyperparameters YAML configs
* **Great training visibility** live progress, GPU stats, charts, startup status

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxV1PO5DbF3ksB51nE2Tw%2Fmore%20cropped%20ui%20for%20homepage.png?alt=media&#x26;token=f75942c9-3d8d-4b59-8ba2-1a4a38de1b86" alt="" width="563"><figcaption></figcaption></figure></div>

### 1. Select model method

#### **Model Type**

Select modality matches use-case:

| Type | Use case |
| -------------- | --------------------------------------- |
| **Text** | Chat, instruction following, completion |
| **Vision** | Image + text (VLMs) |
| **Audio** | Speech / audio understanding |
| **Embeddings** | Sentence embeddings, retrieval |

#### **Training Method**

Three methods available, toggled pill selector:

| Method | Description | VRAM |
| -------------------- | ----------------------------------------- | ------- |
| **QLoRA** | 4-bit quantized base model + LoRA adapter | Lowest |
| **LoRA** | Full-precision base model + LoRA adapter | Medium |
| **Full Fine-tuning** | weights trained | Highest |

Type Hugging Face model name search Hub directly combobox. Local models stored `~/.unsloth/studio/models` Hugging Face cache also appear list.

{% hint style="warning" %}
GGUF format models excluded training - inference.
{% endhint %}

pick model Studio automatically fetches configuration backend pre-fills sensible defaults hyperparameters.

**HuggingFace Token**

Paste Hugging Face access token model gated (e.g. Llama, Gemma). token validated real-time error shown inline invalid.

### 2. Dataset

{% columns %}
{% column %}
Switch two tabs choose data comes :

* **HuggingFace Hub** - live search Hub. last-updated date shown result.
* **Local** - drag--drop click upload file unstructured structured files : `PDF`, `DOCX`, `JSONL`, `JSON`, `CSV`, `Parquet` format. Previously uploaded datasets appear list refreshes automatically.

can view detailed [Datasets Guide here](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide).

Prompt Studio interpret format data:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FCtWUm7GdHnKbe14fUQyT%2Fupdated_dataset.webp?alt=media&#x26;token=3fcefe8d-b6a4-44c2-be9b-6dc282166095" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

| Format | use |
| ---------- | ------------------------------------------- |
| `auto` | Let Unsloth detect format automatically |
| `alpaca` | `instruction` / `input` / `output` columns |
| `chatml` | OpenAI-style `messages` array |
| `sharegpt` | ShareGPT-style conversations |

**Splits Slicing**

* **Subset** - automatically populated dataset card.
* **Train split / Eval split** - choose splits use. Setting eval split enables **Eval Loss** chart training.
* **Dataset slice** - optionally restrict training row range (start index / end index) quick experiments.

**Column Mapping**

Studio automatically map dataset columns correct roles **Dataset Preview dialog** opens. shows sample rows lets assign column `instruction`, `input`, `output`, `image`, etc. Suggested mappings pre-filled possible.

### 3. Hyperparameters

Parameters grouped collapsible sections. can view detailed [LoRA hyperparameters guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) :

{% content-ref url="../../get-started/fine-tuning-llms-guide/lora-hyperparameters-guide" %}
[lora-hyperparameters-guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
{% endcontent-ref %}

| Parameter | Default | Notes |
| ------------------ | ------- | ---------------------------- |
| **Max Steps** | `0` | `0` means use Epochs instead |
| **Context Length** | `2048` | Options: 512 → 32768 |
| **Learning Rate** | `2e-4` | |

**LoRA Settings**

*(Hidden Full Fine-tuning selected)*

| Parameter | Default | Notes |
| ------------------ | ------- | --------------------------------------------------------------------------- |
| **Rank** | `16` | Slider 4–128 |
| **Alpha** | `32` | Slider 4–256 |
| **Dropout** | `0.05` | |
| **LoRA Variant** | `LoRA` | `LoRA` / `RS-LoRA` / `LoftQ` |
| **Target Modules** | | `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |

**Vision** models image dataset, four additional checkboxes appear. Fine-tune:

| Vision Layers | Language Layers | Attention Modules | MLP Modules |
| ------------- | --------------- | ----------------- | ----------- |

**Training Hyperparameters**

Organized three tabs:

{% tabs %}
{% tab title="Optimization" %}

| Parameter | Default |
| --------------------- | ----------- |
| Epochs | 3 |
| Batch Size | 4 |
| Gradient Accumulation | 8 |
| Weight Decay | 0.01 |
| Optimizer | AdamW 8-bit |

{% endtab %}

{% tab title="Schedule" %}

| Parameter | Default |
| ---------------------- | ------- |
| LR Scheduler | linear |
| Warmup Steps | 5 |
| Gradient Checkpointing | unsloth |
| Random Seed | 3407 |
| Save Steps | 0 |
| Eval Steps | 0 |
| Packing | false |
| Train Completions | false |
| {% endtab %} | |

{% tab title="Logging" %}

| Parameter | Default |
| ------------------ | -------------- |
| Enable W\&B | false |
| W\&B Project | llm-finetuning |
| Enable TensorBoard | false |
| TensorBoard Dir | runs |
| Log Frequency | 10 |
| {% endtab %} | |
| {% endtabs %} | |

{% hint style="info" %}
[**Unsloth Gradient Checkpointing**](https://unsloth.ai/docs/blog/500k-context-length-fine-tuning#unsloth-gradient-checkpointing-enhancements)**: `unsloth`** uses Unsloth's custom memory-efficient implementation, can reduce VRAM usage significantly compared standard PyTorch option. recommended default.
{% endhint %}

### 4. Training Config

bottom-right card three config management buttons **Start Training** button.

| Button | Action |
| ---------- | --------------------------------------------- |
| **Upload** | Load previously saved `.yaml` config file |
| **Save** | Export current config YAML |
| **Reset** | Revert parameters model's defaults |

Start Training button stays disabled model dataset configured. Validation errors appear inline - example, setting eval steps without choosing eval split, pairing text-model vision dataset.

#### Loading Screen

{% columns %}
{% column %}
click **Start Training**, full-page overlay appears backend prepares everything.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYtsUxHI0szGw8ZPxCHep%2Fimage.png?alt=media&#x26;token=1701f4af-ef35-48da-80e7-4aba4e80f4d4" alt="" width="375"><figcaption></figcaption></figure></div>
{% endcolumn %}

{% column %}
overlay shows animated terminal live phase updates:

* Blue: Downloading model / dataset
* Amber: Loading model / dataset
* Blue: Configuring
* Green: Training

can cancel time using **×** button corner. confirmation dialog will appear anything stopped.
{% endcolumn %}
{% endcolumns %}

### Training Progress Observability

first training step arrives overlay dismisses live training view revealed. fine-tuning process complete steps reach 100% progress bar. can view elapsed time tokens.&#x20;

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fah3G1rYgRaDNY8Ay6Uw7%2Fimage.png?alt=media&#x26;token=0528c15e-7a4b-4028-8070-95dc0871da5d" alt="" width="563"><figcaption></figcaption></figure></div>

{% columns %}
{% column %}

#### Status Panel

left column shows:

* **Epoch** - current fractional epoch (e.g. `Epoch 1.23`)
* **Progress bar** - step-based, percentage
* **Key metrics**:
 * **Loss** - training loss 4 decimal places
 * **LR** - current learning rate scientific notation
 * **Grad Norm** - gradient norm
 * **Model** - model trained
 * **Method** - `QLoRA` / `LoRA` / `Full`
* **Timing row** - elapsed time, ETA, steps per second, total tokens processed
 {% endcolumn %}

{% column %}

#### GPU Monitor

right column shows live GPU stats polled every seconds:

* **Utilization** - percentage bar
* **Temperature** - °C bar
* **VRAM** - used / total GB
* **Power** - draw / limit watts

#### Stopping Training

Use **Stop Training** button top-right progress card. dialog gives two choices:

* **Stop & Save** - saves checkpoint stopping
* **Cancel** - stops immediately checkpoint
 {% endcolumn %}
 {% endcolumns %}

{% columns %}
{% column %}

#### Charts

Four live charts update training progresses:

1. **Training Loss** - raw values plus EMA-smoothed line running average reference line
2. **Learning Rate** - LR schedule curve
3. **Gradient Norm** - gradient norm steps
4. **Eval Loss** - shown configured eval split
 {% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRgXfe3sobdQWxha8yslr%2Fimage.png?alt=media&#x26;token=b3aa9004-778b-4e3d-85b1-40a205ad0602" alt="" width="278"><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
chart settings (gear icon) :

| Option | Default |
| ------------------ | ------------------- |
| Viewing window | Last N steps slider |
| EMA Smoothing | `0.6` |
| Show Raw | |
| Show Smoothed | |
| Show Average line | |
| Scale (per series) | Linear / Log |
| Outlier clipping | clip / p99 / p95 |
| {% endcolumn %} | |

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFJtjQpAgOFaieyQCYhkq%2Fimage.png?alt=media&#x26;token=4da9cdc2-c088-4ab8-8d0d-40d8d392ee03" alt="" width="276"><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

#### Config Files

{% columns %}
{% column %}
training configurations can saved reloaded YAML files. Files named automatically :

```
{model}_{method}_{dataset}_{timestamp}.yaml
```

{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FuGAKdGkANbh2wIENA9X7%2Fimage.png?alt=media&#x26;token=9553db5b-5c88-4556-be49-fe61035edf11" alt="" width="178"><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

YAML structured three sections:

{% code expandable="true" %}

```yaml
training:
  max_steps: 0
  num_train_epochs: 3
  per_device_train_batch_size: 4
  ...

lora:
  r: 16
  lora_alpha: 32
  ...

logging:
  report_to: none
  ...
```

{% endcode %}

makes easy reproduce runs, share configurations, version-control experiments.

## <i class="fa-hat-chef">:hat-chef:</i> Data Recipes - Quickstart

[Unsloth Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) lets upload documents PDFs CSVs files transforms useable datasets. Create edit datasets visually via graph-node workflow.

recipes page main entry point. Recipes stored locally browser, come back saved work later., can create blank recipe open guided learning recipe.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQ6e19jESrJg0VjHnX58c%2Fdata%20recipes%20final.png?alt=media&#x26;token=8d74e453-815d-4790-83d1-76d0bc80a3ce" alt="" width="563"><figcaption></figcaption></figure></div>

Data Recipes follows basic path. open recipes page, create pick recipe, build workflow editor, validate run preview, run full dataset output looks right. Add seed data generation blocks, validate workflow, preview sample output, run full dataset build. Unsloth Data Recipes powered NVIDIA [DataDesigner](https://github.com/NVIDIA-NeMo/DataDesigner).

glance usual workflow look :

1. Open recipes page.
2. Create new recipe open existing one.
3. Add blocks define dataset workflow.
4. Click **Validate** catch configuration issues early.
5. Run preview inspect sample rows quickly.
6. Run full dataset build recipe ready.
7. Review progress output live graph **Executions** view mode details.
8. Select resulting dataset **Studio** fine tune model.

## <i class="fa-box-isometric">:box-isometric:</i> Export - Quickstart

Use Unsloth Studio 'Export' export, save, convert models GGUF, Safetensors, LoRA deployment, sharing, local inference Unsloth, llama.cpp, Ollama, vLLM,. Export trained checkpoint convert existing model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrrFY8YczW3dDpfYi1k9f%2FScreenshot%202026-03-15%20at%209.28.19%E2%80%AFPM.png?alt=media&#x26;token=d2729e16-799f-48f0-8b07-0248b93fa599" alt="" width="563"><figcaption></figcaption></figure></div>

can read detailed tutorial / guide exporting models Unsloth Studio :

{% content-ref url="export" %}
[export](https://unsloth.ai/docs/new/studio/export)
{% endcontent-ref %}

## <i class="fa-comment-dots">:comment-dots:</i> Chat - Quickstart

[Unsloth Studio Chat](https://unsloth.ai/docs/new/studio/chat) lets run models 100% offline computer. Run model formats GGUF safetensors Hugging Face local files.

* **Download + Run** model GGUFs, fine-tuned adapters, safetensors etc.
* [**Compare** different model](#model-arena) outputs side--side
* **Upload** documents, images, audio prompts
* [**Tune** inference](#generation-settings) settings : temperature, top-p, top-k system prompt

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRCnTAZ6Uh88DIlU3g0Ij%2Fmainpage%20unsloth.png?alt=media&#x26;token=837c96b6-bd09-4e81-bc76-fa50421e9bfb" alt="" width="563"><figcaption></figcaption></figure></div>

can read detailed tutorial / guide running models Unsloth Studio :

{% content-ref url="chat" %}
[chat](https://unsloth.ai/docs/new/studio/chat)
{% endcontent-ref %}

## <i class="fa-video">:video:</i> Video Tutorial

{% hint style="warning" %}
Unsloth Studio versions shown videos old not reflective current version.
{% endhint %}

{% columns fullWidth="true" %}
{% column %}
{% embed url="<https://www.youtube.com/watch?v=mmbkP8NARH4>" %}

video tutorial created NVIDIA get started Studio:
{% endcolumn %}

{% column %}
{% embed url="<https://youtu.be/1lEDuRJWHh4?si=GHaS77ZZPOGjn3GJ>" %}

Install Unsloth Studio Video Tutorial
{% endcolumn %}
{% endcolumns %}

## Advanced Settings

### CLI Commands

Unsloth CLI (`cli.py`) provides following commands:

```
Usage: cli.py [COMMAND]

Commands:
  train             Fine-tune a model
  inference         Run inference on a trained model
  export            Export a trained adapter
  list-checkpoints  List saved checkpoints
  ui                Launch the Unsloth Studio web UI
  studio            Launch the studio (alias)
```

### Project Structure

{% code expandable="true" %}

```
new-ui-prototype/
├── cli.py                     # CLI entry point
├── cli/                       # Typer CLI commands
│   └── commands/
│       ├── train.py
│       ├── inference.py
│       ├── export.py
│       ├── ui.py
│       └── studio.py
├── setup.sh                   # Bootstrap script (Linux / WSL / Colab)
├── setup.ps1                  # Bootstrap script (Windows native)
├── setup.bat                  # Wrapper to launch setup.ps1 via double-click
├── install_python_stack.py    # Cross-platform Python dependency installer
└── studio/
    ├── backend/
    │   ├── main.py            # FastAPI app & middleware
    │   ├── run.py             # Server launcher (uvicorn)
    │   ├── auth/              # Auth storage & JWT logic
    │   ├── routes/            # API route handlers
    │   │   ├── training.py
    │   │   ├── models.py
    │   │   ├── inference.py
    │   │   ├── datasets.py
    │   │   └── auth.py
    │   ├── models/            # Pydantic request/response schemas
    │   ├── core/              # Training engine & config
    │   ├── utils/             # Hardware detection, helpers
    │   └── requirements.txt
    ├── frontend/
    │   ├── src/
    │   │   ├── features/      # Feature modules
    │   │   │   ├── auth/      # Login / signup flow
    │   │   │   ├── training/  # Training config & monitoring
    │   │   │   ├── studio/    # Main studio workspace
    │   │   │   ├── chat/      # Inference chat UI
    │   │   │   ├── export/    # Model export flow
    │   │   │   └── onboarding/# Onboarding wizard
    │   │   ├── components/    # Shared UI components (shadcn)
    │   │   ├── hooks/         # Custom React hooks
    │   │   ├── stores/        # Zustand state stores
    │   │   └── types/         # TypeScript type definitions
    │   ├── package.json
    │   └── vite.config.ts
    └── tests/                 # Backend test suite
```

{% endcode %}

### API Reference

endpoints require valid JWT `Authorization: Bearer <token>` header (except `/api/auth/*` `/api/health`).

| Method | Endpoint | Description |
| ------ | --------------------- | -------------------------------------------------- |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/system` | System info (GPU, CPU, memory) |
| `POST` | `/api/auth/signup` | Create account (requires setup token first run) |
| `POST` | `/api/auth/login` | Login receive JWT tokens |
| `POST` | `/api/auth/refresh` | Refresh expired access token |
| `GET` | `/api/auth/status` | Check auth initialized |
| `POST` | `/api/train/start` | Start training job |
| `POST` | `/api/train/stop` | Stop running training job |
| `POST` | `/api/train/reset` | Reset training state |
| `GET` | `/api/train/status` | Get current training status |
| `GET` | `/api/train/metrics` | Get training metrics (loss, LR, steps) |
| `GET` | `/api/train/stream` | SSE stream real-time training progress |
| `GET` | `/api/models/` | List available models |
| `POST` | `/api/inference/chat` | Send chat message inference |
| `GET` | `/api/datasets/` | List / manage datasets |
