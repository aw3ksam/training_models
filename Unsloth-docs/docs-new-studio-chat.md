---
source_url: "https://unsloth.ai/docs/new/studio/chat"
title: "How to Run models with Unsloth Studio"
converted_at: "2026-04-22T05:11:12.571689"
---

# Run models Unsloth Studio

[Unsloth Studio](https://unsloth.ai/docs/new/studio) lets run AI models 100% offline computer. Run model formats GGUF safetensors Hugging Face local files.

* **Works MacOS, CPU, Windows, Linux, WSL setups! GPU required**
* **Search + Download + Run** model GGUFs, LoRA adapters, safetensors etc.
* [**Compare**](#model-arena) two different model outputs side--side
* [**Self-healing tool calling**](#auto-healing-tool-calling) / web search, [**code execution**](#code-execution) call OpenAI-compatible APIs
* [**Auto inference parameter**](#auto-parameter-tuning) tuning (temp, top-p etc.) edit chat templates
* Upload images, audio, PDFs, code, DOCX file types chat.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Ft1WkYzHmOVMXumiz71N0%2Ftoolcalling%20chat%20preview.png?alt=media&#x26;token=a1741a6c-bf24-4df8-9f27-ce21b868dbdf" alt="" width="563"><figcaption></figcaption></figure></div>

### Using Unsloth Studio Chat

{% columns %}
{% column %}

#### Search run models

can search download model via Hugging Face use local files.

Studio supports wide range model types, including **GGUF**, vision-language, text--speech models. Run latest models [Qwen3.5](https://unsloth.ai/docs/models/qwen3.5) NVIDIA [Nemotron 3](https://unsloth.ai/docs/models/nemotron-3).

Upload images, audio, PDFs, code, DOCX file types chat.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBf3UDywdNSlvCBhUuVsp%2FScreenshot%202026-03-17%20at%2012.34.23%E2%80%AFAM.png?alt=media&#x26;token=b6127cbf-76f7-48da-b869-3760ed5e9b42" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
Unsloth Studio Chat automatically works **multi-GPU setups** inference.
{% endhint %}

{% columns %}
{% column %}

#### Code execution

Unsloth Studio lets LLMs run Bash Python, not JavaScript. also sandboxes programs Claude Artifacts models can test code, generate files, verify answers real computation.

makes answers models reliable accurate.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fel6jjv4rUTRCRwcRpIr7%2Flong%20code%20exec.png?alt=media&#x26;token=9d3d5930-0fdc-4d97-941c-983e5629296d" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

#### Auto-healing tool calling

Unsloth Studio not allows tool calling web search, also auto-fixes errors might happen.

means always get inference outputs **without** broken tool calling.&#x20;

E.g. Qwen3.5-4B searched 20+ websites cited sources, web search happening inside thinking trace.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXPQGEEr1YoKofrTatAKK%2Ftoolcallingif.gif?alt=media&#x26;token=25d68698-fb13-4c46-99b2-d39fb025df08" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

#### Auto parameter tuning

Inference parameters **temperature**, **top-p**, **top-k** automatically pre-set new models Qwen3.5 can get best outputs without worrying settings. can also adjust parameters manually edit system prompt.

Context length adjustment longer necessary llama.cpp’s smart auto context, uses context need without loading anything extra.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAQKsjtynvCXKtadvKhq1%2FRecording%202026-03-13%20114257.gif?alt=media&#x26;token=b5bfff0c-8189-4358-9344-08d0ae17782a" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}

#### Chat Workspace

Enter prompts, attach documents, images (webp, png), code files, txt, audio additional context, see model’s responses real time.

Toggle : Thinking + Web search.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHlOKWnSB6slhE1EXgAeZ%2Fimage.png?alt=media&#x26;token=b5bdfe4e-fe0e-4a2a-9eba-b04b15a79018" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

### Model Arena

Studio Chat lets compare two models side--side using prompt. E.g. compare base model LoRa adapter. Inference will firstly load one model, second one (parallel inference worked ).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FC3xjqlunbpUr7nx6sQ4j%2Fimage.png?alt=media&#x26;token=65501d63-1346-4a1e-b055-c94294a24305" alt="" width="563"><figcaption></figcaption></figure></div>

{% columns %}
{% column %}
training, can compare base fine-tuned models side side prompt see changed whether results improved.

workflow makes easy see fine-tuning changed model’s responses whether improved results use case.
{% endcolumn %}

{% column %}

<div align="center" data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVgnE7eMPQk2vaFboJ4BU%2Fmodel%20arena%20closeup.png?alt=media&#x26;token=8b0a910b-440c-4859-a846-0060e61e157b" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
Unsloth Studio Chat auto works **multi-GPU setups** inference.
{% endhint %}

### Using old / existing GGUF models

{% columns %}
{% column %}
**Apr 1 update:** can now select existing folder Unsloth detect.

**Mar 27 update:** Unsloth Studio now **automatically detects older / pre-existing models** downloaded Hugging Face, LM Studio etc.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBn3Fs1cchFchl328wSOs%2FScreenshot%202026-04-05%20at%205.43.57%E2%80%AFAM.png?alt=media&#x26;token=cc57ec6e-653a-4824-8e8d-a6bfbcd27493" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

**Manual instructions:** Unsloth Studio detects models downloaded Hugging Face Hub cache `(C:\Users{your_username}.cache\huggingface\hub)`. GGUF models downloaded LM Studio, note stored `C:\Users\{your_username}.cache\lm-studio\models` ****** `C:\Users{your_username}\lm-studio\models` not visible llama.cpp default - will need move copy.gguf files Hugging Face Hub cache directory (another path accessible llama.cpp) Unsloth Studio load.

fine-tuning model adapter Studio, can export GGUF run local inference **llama.cpp** directly Studio Chat. Unsloth Studio powered llama.cpp Hugging Face.

### Adding Files Context

Studio Chat supports multimodal inputs directly conversation. can attach documents, images, audio additional context prompt.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FSitddQpGkOwUvirMem5P%2Fimage.png?alt=media&#x26;token=43b7af91-ea86-4279-a787-b4b444640d82" alt="" width="563"><figcaption></figcaption></figure></div>

makes easy test model handles real-world inputs PDFs, screenshots, reference material. Files processed locally included context model.

### **Deleting model files**

can delete old model files either bin icon model search removing relevant cached model folder default Hugging Face cache directory. default, Hugging Face uses `~/.cache/huggingface/hub/` macOS/Linux/WSL `C:\Users\<username>\.cache\huggingface\hub\` Windows.

* **MacOS, Linux, WSL:** `~/.cache/huggingface/hub/`
* **Windows:** `%USERPROFILE%\.cache\huggingface\hub\`

`HF_HUB_CACHE` `HF_HOME` set, use location instead. Linux WSL, `XDG_CACHE_HOME` can also change default cache root.

### **Unsloth not detecting using GPU**

model not using GPU specifically Docker, try:

Pulling latest image manually:

```bash
 docker pull unsloth/unsloth:latest
```

* Start container GPU access:
 * `docker run`: `--gpus all`
 * Docker Compose: `capabilities: [gpu]`
* Linux, make sure NVIDIA Container Toolkit installed.
* Windows:
 * Check `nvcc --version` matches CUDA version shown `nvidia-smi`
 * Follow: <https://docs.docker.com/desktop/features/gpu/>
