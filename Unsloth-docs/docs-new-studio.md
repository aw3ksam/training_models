---
source_url: "https://unsloth.ai/docs/new/studio"
title: "Introducing Unsloth Studio"
converted_at: "2026-04-22T05:11:12.863423"
---

# Introducing Unsloth Studio

Today, ’re launching **Unsloth Studio** (Beta): open-source, -code web UI training, running exporting open models one unified **local** interface.

<a href="#quickstart" class="button primary" data-icon="bolt">Quickstart</a><a href="#features" class="button secondary" data-icon="star">Features</a><a href="https://github.com/unslothai/unsloth" class="button secondary" data-icon="github">Github</a>

* **Run GGUF** safetensor models locally **Mac**, Windows, Linux.
* Train 500+ models 2x faster 70% less VRAM (accuracy loss)
* Run train text, vision, TTS audio, embedding models

{% hint style="success" %}
**latest updates, see ** [**new changelog page here**](https://unsloth.ai/docs/new/changelog)**!** ✨
{% endhint %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxV1PO5DbF3ksB51nE2Tw%2Fmore%20cropped%20ui%20for%20homepage.png?alt=media&#x26;token=f75942c9-3d8d-4b59-8ba2-1a4a38de1b86" alt=""><figcaption></figcaption></figure></div>

* **MacOS** **CPU** work [Chat](#run-models-locally) GGUF inference [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe). MLX training coming soon.
* dataset needed. [**Auto-create datasets**](https://unsloth.ai/docs/new/studio/data-recipe) **PDF, CSV, JSON, DOCX, TXT** files.
* [Export or save](https://unsloth.ai/docs/new/studio/export) model GGUF, 16-bit safetensor etc.
* [**Self-healing tool calling**](https://unsloth.ai/docs/new/chat#auto-healing-tool-calling) / web search + [**code execution**](https://unsloth.ai/docs/new/chat#code-execution)
* [Auto inference parameter](https://unsloth.ai/docs/new/chat#auto-parameter-tuning) tuning edit chat templates.

## ⭐ Features

{% columns %}
{% column %}

### **Run models locally**

[Search and run GGUF](https://unsloth.ai/docs/new/studio/chat) safetensor models [self-healing tool](https://unsloth.ai/docs/new/chat#auto-healing-tool-calling) calling / web search, [auto inference](https://unsloth.ai/docs/new/chat#auto-parameter-tuning) parameter tuning, [**code execution**](https://unsloth.ai/docs/new/chat#code-execution) (Bash + Python), APIs (soon). Upload images, docs, audio, code.

[Battle models side by side](#model-arena). Powered llama.cpp + Hugging Face, support **multi-GPU inference** models.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFeQ0UUlnjXkDdqhcWglh%2Fskinny%20studio%20chat.png?alt=media&#x26;token=c2ee045f-c243-4024-a8e4-bb4dbe7bae79" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Execute code + heal Tool calling

Unsloth Studio lets LLMs run Bash Python, not JavaScript. also sandboxes programs Claude Artifacts models can test code, generate files, verify answers real computation.

E.g. Qwen3.5-4B searched 20+ websites cited sources, web search happening inside thinking trace.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXPQGEEr1YoKofrTatAKK%2Ftoolcallingif.gif?alt=media&#x26;token=25d68698-fb13-4c46-99b2-d39fb025df08" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### **-code training**

[Upload PDF, CSV, JSON](#data-recipes) docs, YAML configs start training instantly NVIDIA. Unsloth’s kernels optimize LoRA, FP8, FFT, PT across 500+ text, vision, TTS/audio embedding models.

Fine-tune latest LLMs [Qwen3.5](https://unsloth.ai/docs/models/qwen3.5/fine-tune) NVIDIA [Nemotron 3](https://unsloth.ai/docs/models/nemotron-3). [Multi-GPU](https://unsloth.ai/docs/basics/multi-gpu-training-with-unsloth) works automatically, new version coming.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRjAfHShyL7MfHfq6BStl%2Fonboarding%20updated.png?alt=media&#x26;token=7cdde1a0-8f8c-4d25-9414-e28f35f211cd" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Data Recipes

[**Data Recipes**](https://unsloth.ai/docs/new/studio/data-recipe) transforms docs useable / synthetic datasets via graph-node workflow. Upload unstructured structured files PDFs, CSV JSON. Unsloth Data Recipes, powered NVIDIA Nemo [Data Designer](https://github.com/NVIDIA-NeMo/DataDesigner), auto turns documents desired formats.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fcc9T0V8WsyjcuOE2sIVV%2Fdata%20recipes%20longer.png?alt=media&#x26;token=5ae33e8d-09b1-45e0-8f5c-40dca8bbcf0c" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Observability

Gain [complete visibility](https://unsloth.ai/docs/new/start#training-progress) control training runs. Track training loss, gradient norms, GPU utilization real time, customize liking.

can even view training progress devices phone.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FCIrWHN1JzfaFNOoavmZS%2Fobserve%20new.png?alt=media&#x26;token=21fdbc5b-a073-437a-b487-b5bdff4716f6" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Export / Save models

[**Export any model**](https://unsloth.ai/docs/new/studio/export), including fine-tuned models, safetensors, GGUF use llama.cpp, vLLM, Ollama, LM Studio,.

Stores training history, can revisit runs, export experiment.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8UHzGTHF9q6LWrJy8Y4r%2FScreenshot%202026-03-15%20at%203.02.02%E2%80%AFAM.png?alt=media&#x26;token=cb5e78f8-481a-4c9f-9361-db53e6e0ec37" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Model Arena

Chat [compare 2 different](https://unsloth.ai/docs/new/chat#model-arena) models, base model fine-tuned one, see outputs differ.

load first GGUF/model, second, voilà! Inference will firstly load one model, second one.
{% endcolumn %}

{% column %}

<div align="center" data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVgnE7eMPQk2vaFboJ4BU%2Fmodel%20arena%20closeup.png?alt=media&#x26;token=8b0a910b-440c-4859-a846-0060e61e157b" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

### Privacy first + Secure

Unsloth Studio can used 100% offline locally computer. token-based authentication, including encrypted password JWT access / refresh flows keeps data secure.

can use pre-exisiting / old models GGUFs previously downloaded HF etc. Read [instructions here](https://unsloth.ai/docs/new/chat#using-old-existing-gguf-models).
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F15gRLbMDX1ReKdHBBl1G%2FScreenshot%202026-03-15%20at%203.54.51%E2%80%AFAM.png?alt=media&#x26;token=ca096807-54c2-4d8c-bdc1-c1bb0055469b" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="warning" %}
Please note **BETA** version Unsloth Studio. Expect many improvements, fixes, new features coming days weeks.
{% endhint %}

## ⚡ Quickstart

Unsloth Studio works Windows, Linux, WSL MacOS (chat currently).

* **CPU:** Unsloth still works without GPU, [Chat](#run-models-locally) inference [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe).
* **Training:** Works **NVIDIA**: RTX 30, 40, 50, Blackwell, DGX Spark/Station etc. + **Intel** GPUs
* **Mac:** CPU - Chat [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) works now. **MLX** training coming soon.
* **AMD:** Chat works. Train [Unsloth Core](https://unsloth.ai/docs/get-started/install/amd). Studio support coming soon.
* **Coming soon:** Training support **Apple MLX** **AMD.**
* **Multi-GPU:** Works already, major upgrade way.

Use install commands update:

### **MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

### **Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

#### Launch Unsloth

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

### Docker:

Use official **Docker image**: [`unsloth/unsloth`](https://hub.docker.com/r/unsloth/unsloth) currently works Windows, WSL Linux. MacOS support coming soon.

{% code overflow="wrap" expandable="true" %}

```bash
docker run -d -e JUPYTER_PASSWORD="mypassword" \
  -p 8888:8888 -p 8000:8000 -p 2222:22 \
  -v $(pwd)/work:/workspace/work \
  --gpus all \
  unsloth/unsloth
```

{% endcode %}

{% hint style="success" %}
**First install now 6x faster 50% reduced size due precompiled llama.cpp binaries.**
{% endhint %}

**details install uninstallation please visit ** [**Unsloth Studio Install**](https://unsloth.ai/docs/new/studio/install) **section.**

{% content-ref url="studio/install" %}
[install](https://unsloth.ai/docs/new/studio/install)
{% endcontent-ref %}

### <i class="fa-google">:google:</i> Google Colab notebook

’ve created [free Google Colab notebook](https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb) can explore Unsloth’s features Colab’s T4 GPUs. can train run models 22B parameters, switch larger GPU bigger models. Click 'Run ' UI pop installation.

{% columns %}
{% column %}
{% embed url="<https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb>" %}

installation complete, scroll **Start Unsloth Studio** click **Open Unsloth Studio** white box shown left:

**Scroll, see actual UI.**
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FkYitMrK55Ic6eIGqiKEJ%2FScreenshot%202026-03-16%20at%2011.21.16%E2%80%AFPM.png?alt=media&#x26;token=4388c309-a598-41f3-9301-e434c334ac1c" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="warning" %}
Sometimes Studio link may return error. happens might disabled cookies using adblocker Mozilla. can still access UI scrolling button.
{% endhint %}

## <i class="fa-seedling">:seedling:</i> Workflow

usual workflow Unsloth Studio get started:

1. Launch Studio [install instructions](https://unsloth.ai/docs/new/studio/install).
2. Load model local files supported integration.
3. Import training data PDFs, CSVs, JSONL files, build dataset scratch.
4. Clean, refine, expand dataset [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe).
5. Start training recommended presets customize config.
6. Chat trained model compare outputs base model.
7. [Save or export](#export-save-models) locally stack already use.

can read individual deep dives section Unsloth Studio:

{% columns %}
{% column width="50%" %}
{% content-ref url="studio/start" %}
[start](https://unsloth.ai/docs/new/studio/start)
{% endcontent-ref %}

{% content-ref url="studio/export" %}
[export](https://unsloth.ai/docs/new/studio/export)
{% endcontent-ref %}
{% endcolumn %}

{% column width="50%" %}
{% content-ref url="studio/data-recipe" %}
[data-recipe](https://unsloth.ai/docs/new/studio/data-recipe)
{% endcontent-ref %}

{% content-ref url="studio/chat" %}
[chat](https://unsloth.ai/docs/new/studio/chat)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

## <i class="fa-video">:video:</i> Video Tutorials

{% hint style="warning" %}
Unsloth Studio versions shown videos old not reflective current version.
{% endhint %}

{% columns fullWidth="false" %}
{% column %}
{% embed url="<https://www.youtube.com/watch?v=mmbkP8NARH4>" fullWidth="false" %}

video tutorial created NVIDIA get started Studio:
{% endcolumn %}

{% column %}
{% embed url="<https://youtu.be/1lEDuRJWHh4?si=GHaS77ZZPOGjn3GJ>" %}

Install Unsloth Studio Video Tutorial
{% endcolumn %}
{% endcolumns %}

## <i class="fa-comments-question">:comments-question:</i> FAQ

**Unsloth collect store data?**\
Unsloth not collect usage telemetry. Unsloth collects minimal hardware information required compatibility, GPU type device (e.g. Mac). Unsloth Studio runs 100% offline locally.

**use old / exisiting model downloaded previously Hugging Face?**\
Yes, can use pre-exisiting/old models GGUFs previously downloaded Hugging Face etc. now automatically detected Unsloth otherwise read [instructions here](https://unsloth.ai/docs/new/chat#using-old-existing-gguf-models).

**inference sometimes slower Unsloth?**\
Unsloth, local inference apps, powered llama.cpp, speeds mostly. Sometimes Unsloth might turned web-search, code execution, self-healing tool-calling. features may make inference slower. speed difference still slower features turned, please make GitHub issue!

**Unsloth Studio support OpenAI-compatible APIs?**\
Yes, Data Recipes. inference working hope release support soon week stay tuned!

**Unsloth now licensed AGPL-3.0?**\
Unsloth uses dual-licensing model Apache 2.0 AGPL-3.0. core Unsloth package remains licensed [**Apache 2.0**](https://github.com/unslothai/unsloth?tab=Apache-2.0-1-ov-file), certain optional components, Unsloth Studio UI licensed [**AGPL-3.0**](https://github.com/unslothai/unsloth?tab=AGPL-3.0-2-ov-file).

structure helps support ongoing Unsloth development keeping project open source enabling broader ecosystem continue growing.

**Studio support LLMs?**\
. Studio supports range supported `transformers` compatible model families, including text, multimodal models, [text-to-speech](https://unsloth.ai/docs/basics/text-to-speech-tts-fine-tuning), audio, [embeddings](https://unsloth.ai/docs/basics/embedding-finetuning), BERT-style models.

**Can use training config?**\
Yes. Import YAML config Studio will pre-fill relevant settings.

**can adjust context length?**\
Context length adjustment longer necessary llama.cpp’s smart auto context, uses context need without loading anything extra. However, soon will still add feature incase want use.

**need train models use UI?**\
, can download GGUF model without fine-tuning model.

#### Future Unsloth

working hard make open-source AI accessible possible. Coming next Unsloth Unsloth Studio, releasing official support : multi-GPU, Apple Silicon/MLX AMD. Reminder BETA version Unsloth Studio expect lot announcements improvements coming weeks. ’re also working closely NVIDIA multi-GPU support deliver best simplest experience possible.

#### Acknowledgements

huge thank NVIDIA Hugging Face part launch. Also thanks early beta testers Unsloth Studio, truly appreciate time feedback. ’d also thank llama.cpp, PyTorch open model labs providing infrastructure made Unsloth Studio possible.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLsNFO8j8Sdovm8x2gY2n%2Fsloth%20painting.png?alt=media&#x26;token=650b3dc4-0bd4-4d30-9443-c23f67bfef7a" alt="" width="375"><figcaption></figcaption></figure>
