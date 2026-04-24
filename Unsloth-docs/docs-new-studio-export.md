---
source_url: "https://unsloth.ai/docs/new/studio/export"
title: "Export models with Unsloth Studio"
converted_at: "2026-04-22T05:11:12.718034"
---

# Export models Unsloth Studio

Use [Unsloth Studio](https://unsloth.ai/docs/new/studio) export, save, convert models GGUF, Safetensors, LoRA deployment, sharing, local inference Unsloth, llama.cpp, Ollama, vLLM,. Export trained checkpoint convert existing model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrrFY8YczW3dDpfYi1k9f%2FScreenshot%202026-03-15%20at%209.28.19%E2%80%AFPM.png?alt=media&#x26;token=d2729e16-799f-48f0-8b07-0248b93fa599" alt="" width="563"><figcaption></figcaption></figure></div>

{% stepper %}
{% step %}

### Select Training Run

Start selecting training run want export. run represents complete training session may contain multiple checkpoints.

choosing run, select checkpoint export. checkpoint saved version model created training.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FzB12XFNP3UjoAT1l9vz3%2Fimage.png?alt=media&#x26;token=021b8864-b2c5-4a92-927e-e23350610036" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

### Select Checkpoint

Later checkpoints typically represent final trained model, can export checkpoint depending needs.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8VfRPUcY3w6zYfNmAIDn%2Fimage.png?alt=media&#x26;token=42565a7d-e62f-4cf0-bd33-90422f1b2194" alt="" width="560"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

### Export Methods

Depending workflow, can export merged model, LoRA adapter weights, GGUF model local inference.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fh4sPts9rJhHiGqf0UxIs%2Fimage.png?alt=media&#x26;token=4f1d6a76-bd40-4471-ab8d-0b2fe33d0410" alt=""><figcaption></figcaption></figure></div>

export method produces different version model depending plan run share. table explains option exports.

| Export Type | Description |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| Merged Model | **16-bit model** LoRA adapter merged base weights. |
| LoRA | Exports **adapter weights**. Requires original base model. |
| GGUF / llama.cpp | Converts model **GGUF format** Unsloth / llama.cpp **/** Ollama / LM Studio inference. |
| {% endstep %} | |

{% step %}

### Export / Save Locally

exporting model, can choose resulting files saved. Models can downloaded directly machine pushed Hugging Face Hub hosting sharing.

Save exported model files directly machine. option useful running model locally, distributing files manually, integrating local inference tools.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfsBaE8V2o69jSyCVGIz4%2Fimage.png?alt=media&#x26;token=4ef3fa06-d25b-424a-91e3-42debd3b6908" alt="" width="325"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

### Push Hub

Upload exported model Hugging Face Hub. allows host, share, deploy model central repository.

will need Hugging Face write token publish model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrvVnuVUYQWv2nkrgFxpK%2Fimage.png?alt=media&#x26;token=5e0b91fe-5225-4bff-9fa9-ec1fb3867b1a" alt="" width="325"><figcaption></figcaption></figure></div>

{% hint style="success" %}
already authenticated Hugging Face CLI, write token can left empty.
{% endhint %}
{% endstep %}
{% endstepper %}
