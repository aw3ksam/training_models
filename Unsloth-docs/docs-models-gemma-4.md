---
source_url: "https://unsloth.ai/docs/models/gemma-4"
title: "Gemma 4 - How to Run Locally"
converted_at: "2026-04-22T05:11:04.939905"
---

# Gemma 4 - Run Locally

Gemma 4 Google DeepMind’s new family open models, including **E2B**, **E4B**, **26B-A4B**, **31B.** multimodal, hybrid-thinking models support 140+ languages, **256K context**, dense MoE variants. Gemma 4 Apache-2.0 licensed can run local device.

{% columns %}
{% column %} <a href="#run-gemma-4-tutorials" class="button primary">Run Gemma 4</a><a href="gemma-4/train" class="button secondary">Fine-tune Gemma 4</a>

**Gemma-4-E2B** **E4B** support image audio. Run **5GB RAM** (4-bit) 15GB (full 16-bit). See [Gemma 4 GGUFs](https://huggingface.co/collections/unsloth/gemma-4).

**Gemma-4-26B-A4B** runs **18GB** (4-bit) 28GB (8-bit). **Gemma-4-31B** needs **20GB RAM** (4-bit) 34GB (8-bit).
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FstfdTMsoBMmsbQsgQ1Ma%2Flandscape%20clip%20gemma.gif?alt=media&#x26;token=eec5f2f7-b97a-4c1c-ad01-5a041c3e4013" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
**Apr 20:** conducted [Gemma 4 GGUF Benchmarks](#unsloth-gguf-benchmarks) help pick best quant.

**Apr 11 update:** Gemma 4 now updated Google's updated chat template + llama.cpp fixes.\
**NOT** use CUDA 13.2 runtime GGUF will cause poor outputs.

can now run GGUFs fine-tune Gemma 4 [Unsloth Studio](#unsloth-studio-guide)✨
{% endhint %}

### Usage Guide

Gemma 4 excels reasoning, coding, tool use, long-context agentic workflows, multimodal tasks. smaller E2B E4B variants designed phones laptops, larger models target medium-high CPU /VRAM systems PCs NVIDIA RTX GPUs.

| Gemma 4 Variant | Details | Best fit |
| --------------- | ----------------------------------------------------------------- | ----------------------------------------------------- |
| **E2B** | <p>Dense + PLE (128K context)<br>Supports: Text, Image, Audio</p> | phone / edge inference, ASR, speech translation |
| **E4B** | <p>Dense + PLE (128K context)<br>Support: Text, Image, Audio</p> | Small model laptops fast local multimodal use |
| **26B-A4B** | <p>MoE (256K context)<br>Support: Text, Image</p> | Best speed / quality tradeoff computer use |
| **31B** | <p>Dense (256K context)<br>Support: Text, Image</p> | Strongest performance slower inference |

**See Gemma 4:** [**Performance benchmarks**](#official-gemma-benchmarks) **** [**GGUF benchmarks**](#unsloth-gguf-benchmarks)**.**

**pick 26B-A4B 31B?**

* **26B-A4B** - balances speed accuracy. MoE design makes faster 31B, 4B active parameters. Pick RAM limited fine trading bit quality speed.
* **31B** - currently strongest Gemma 4 model. Pick maximum quality enough memory can accept slightly slower speeds.

### Hardware requirements

**Table: Gemma 4 Inference GGUF recommended hardware requirements** (units = total memory: RAM + VRAM, unified memory). can use Gemma 4 MacOS, NVIDIA RTX GPUs etc.

| Gemma 4 variant | 4-bit | 8-bit | BF16 / FP16 |
| --------------- | -------: | -------: | ----------: |
| **E2B** | 4 GB | 5–8 GB | 10 GB |
| **E4B** | 5.5–6 GB | 9–12 GB | 16 GB |
| **26B A4B** | 16–18 GB | 28–30 GB | 52 GB |
| **31B** | 17–20 GB | 34–38 GB | 62 GB |

{% hint style="info" %}
rule thumb, total available memory least exceed size quantized model download. not, llama.cpp can still run using partial RAM / disk offload, generation will slower. will also need compute, depending context window use.
{% endhint %}

### Recommended Settings

recommended use Google's default Gemma 4 parameters:

* `temperature = 1.0`
* `top_p = 0.95`
* `top_k = 64`

Recommended practical defaults local inference:

* Start **32K context** responsiveness, increase
* Keep **repetition/presence penalty** disabled 1.0 unless see looping.
* End Sentence token `<turn|>`

{% hint style="info" %}
Gemma 4's max context **128K** **E2B / E4B** **256K** **26B A4B / 31B**.
{% endhint %}

#### Thinking Mode

Compared older Gemma chat templates, Gemma 4 uses standard **`system`**, **`assistant`**, **`user`** roles adds explicit thinking control.

**enable thinking:**

Add token **`<|think|>`** **start system prompt**.

{% columns %}
{% column %}
**Thinking enabled**

```
<|think|>
You are a careful coding assistant. Explain your answer clearly.
```

{% endcolumn %}

{% column %}
**Thinking disabled**

```
You are a careful coding assistant. Explain your answer clearly.
```

{% endcolumn %}
{% endcolumns %}

**Output behavior:**

{% columns %}
{% column %}
thinking enabled, model outputs internal reasoning channel final answer.

```
<|channel>thought
[internal reasoning]
<channel|>
[final answer]
```

{% endcolumn %}

{% column %}
thinking disabled, larger models may still emit **empty thought block** final answer.

```
<|channel>thought
<channel|>
[final answer]
```

{% endcolumn %}
{% endcolumns %}

**example using "**&#x57;hat capital France?":

{% code overflow="wrap" %}

```
<bos><|turn>system\n<|think|><turn|>\n<|turn>user\nWhat is the capital of France?<turn|>\n<|turn>model\n
```

{% endcode %}

**outputs :**

{% code overflow="wrap" %}

```
<|channel>thought\nThe user is asking for the capital of France.\nThe capital of France is Paris.<channel|>The capital of France is Paris.<turn|>
```

{% endcode %}

**Multi-turn chat rule:**

multi-turn conversations, **keep final visible answer chat history**. **not** feed prior thought blocks back next turn.

{% code overflow="wrap" %}

```
<bos><|turn>user\nWhat is 1+1?<turn|>\n<|turn>model\n2<turn|>\n<|turn>user\nWhat is 1+1?<turn|>\n<|turn>model\n2<turn|>\n<|turn>user\nWhat is 1+1?<turn|>\n<|turn>model\n2<turn|>\n<|turn>user\nWhat is 1+1?<turn|>\n<|turn>model\n2<turn|>\n
```

{% endcode %}

**disable thinking:**

Note `llama-cli` might not work reliably, use `llama-server` disabling reasoning:

{% hint style="warning" %}
[disable thinking / reasoning](#how-to-enable-or-disable-reasoning-and-thinking), use `--chat-template-kwargs '{"enable_thinking":false}'`

**Windows** Powershell, use: `--chat-template-kwargs "{\"enable_thinking\":false}"`

Use 'true' 'false' interchangeably.
{% endhint %}

## Run Gemma 4 Tutorials

Gemma 4 GGUFs comes several sizes, recommended starting point small models 8-bit larger models **Dynamic 4-bit**. [Gemma 4 GGUFs](https://huggingface.co/collections/unsloth/gemma-4) [MLX](#mlx-dynamic-quants):

| [gemma-4-E2B](https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF) | [gemma-4-E4B](https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF) | [gemma-4-26B-A4B](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF) | [gemma-4-31B](https://huggingface.co/unsloth/gemma-4-31B-it-GGUF) |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------- |

<a href="#unsloth-studio-guide" class="button primary">🦥 Unsloth Studio Guide</a><a href="#llama.cpp-guide" class="button primary">🦙 Llama.cpp Guide</a>

{% columns %}
{% column %}
**can run train Gemma 4 free UI ** [**Unsloth Studio**](https://unsloth.ai/docs/new/studio)✨ **notebook:**
{% endcolumn %}

{% column %}
{% embed url="<https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb>" %}
{% endcolumn %}
{% endcolumns %}

### 🦥 Unsloth Studio Guide

Gemma 4 can now run fine-tuned [Unsloth Studio](https://unsloth.ai/docs/new/studio), new open-source web UI local AI. Unsloth Studio lets run models locally **MacOS, Windows**, Linux :

{% columns %}
{% column %}

* Search, download, [run GGUFs](https://unsloth.ai/docs/new/studio#run-models-locally) safetensor models
* [**Self-healing** tool calling](https://unsloth.ai/docs/new/studio#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](https://unsloth.ai/docs/new/studio#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/new/studio#model-arena) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](https://unsloth.ai/docs/new/studio#no-code-training) 2x faster 70% less VRAM
 {% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVrLgXwplAMcvkU4owjPk%2F26b%20gif.gif?alt=media&#x26;token=8a569952-c152-435f-b815-c9f295619587" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

Run terminal:

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Launch Unsloth

**MacOS, Linux, WSL Windows:**

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

**open `http://localhost:8888` browser.**
{% endstep %}

{% step %}

#### Search download Gemma 4

first launch will need create password secure account sign later. ’ll see brief onboarding wizard choose model, dataset, basic settings. can skip time.

go [Studio Chat](https://unsloth.ai/docs/new/studio/chat) tab search Gemma 4 search bar download desired model quant.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpYoNILI8NFMl8QaQlc7V%2FScreenshot%202026-04-02%20at%2010.37.32%E2%80%AFPM.png?alt=media&#x26;token=18d5918e-4f71-4e0e-b8c9-464097389835" alt="" width="375"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

#### Run Gemma 4

Inference parameters auto-set using Unsloth Studio, however can still change manually. can also edit context length, chat template settings.

information, can view [Unsloth Studio inference guide](https://unsloth.ai/docs/new/studio/chat).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVrLgXwplAMcvkU4owjPk%2F26b%20gif.gif?alt=media&#x26;token=8a569952-c152-435f-b815-c9f295619587" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Llama.cpp Guide

guide will utilizing Dynamic 4-bit 26B-A4B 31B 8-bit E2B E4B. See: [Gemma 4 GGUF collection](https://huggingface.co/collections/unsloth/gemma-4)

tutorials, will using [llama.cpp](https://llama.cpphttps/github.com/ggml-org/llama.cpp) fast local inference, especially CPU.

{% stepper %}
{% step %}
Obtain latest `llama.cpp` **** [**GitHub here**](https://github.com/ggml-org/llama.cpp). can follow build instructions. Change `-DGGML_CUDA=ON` `-DGGML_CUDA=OFF` GPU want CPU inference. **Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` continue usual - Metal support default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
want use `llama.cpp` directly load models, can follow commands, according model. `UD-Q4_K_XL` quantization type. can also download via Hugging Face (step 3). similar `ollama run`. Use `export LLAMA_CACHE="folder"` force `llama.cpp` save specific location. need set context length llama.cpp automatically uses exact amount required.

**26B-A4B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-26B-A4B-it-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**31B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-31B-it-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-31B-it-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**E4B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-E4B-it-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-E4B-it-GGUF:Q8_0 \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**E2B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-E2B-it-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-E2B-it-GGUF:Q8_0 \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

{% endstep %}

{% step %}
Download model via (installing `pip install huggingface_hub hf_transfer` ). can choose `UD-Q4_K_XL` quantized versions `Q8_0`. downloads get stuck, see: [hugging-face-hub-xet-debugging](https://unsloth.ai/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging "mention")

```bash
hf download unsloth/gemma-4-26B-A4B-it-GGUF \
    --local-dir unsloth/gemma-4-26B-A4B-it-GGUF \
    --include "*mmproj-BF16*" \
    --include "*UD-Q4_K_XL*" # Use "*UD-Q2_K_XL*" for Dynamic 2bit
```

{% endstep %}

{% step %}
run model conversation mode (vision `mmproj-F16`):

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf \
    --mmproj unsloth/gemma-4-26B-A4B-it-GGUF/mmproj-BF16.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

{% endcode %}
{% endstep %}

{% step %}

### Llama-server deployment

deploy Gemma-4 llama-server, use:

```bash
./llama.cpp/llama-server \
    --model unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf \
    --mmproj unsloth/gemma-4-26B-A4B-it-GGUF/mmproj-BF16.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64 \
    --alias "unsloth/gemma-4-26B-A4B-it-GGUF" \
    --port 8001 \
    --chat-template-kwargs '{"enable_thinking":true}'
```

{% hint style="warning" %}
[disable thinking / reasoning](#how-to-enable-or-disable-reasoning-and-thinking), use `--chat-template-kwargs '{"enable_thinking":false}'`

**Windows** Powershell, use: `--chat-template-kwargs "{\"enable_thinking\":false}"`

Use 'true' 'false' interchangeably.
{% endhint %}
{% endstep %}
{% endstepper %}

### MLX Dynamic Quants

also uploaded dynamic 4bit 8bit quants first trial MacOS device!

{% hint style="success" %}
Now **vision** support!
{% endhint %}

| Gemma 4 | 4-bit MLX | 8-bit MLX |
| ------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 31B | [link](https://huggingface.co/unsloth/gemma-4-31b-it-UD-MLX-4bit) | [link](https://huggingface.co/unsloth/gemma-4-31b-it-MLX-8bit) |
| 26B-A4B | [link](https://huggingface.co/unsloth/gemma-4-26b-a4b-it-UD-MLX-4bit) | [link](https://huggingface.co/unsloth/gemma-4-26b-a4b-it-MLX-8bit) |
| E4B | [link](https://huggingface.co/unsloth/gemma-4-E4B-it-UD-MLX-4bit) | [link](https://huggingface.co/unsloth/gemma-4-E4B-it-MLX-8bit) |
| E2B | [link](https://huggingface.co/unsloth/gemma-4-E2B-it-UD-MLX-4bit) | [link](https://huggingface.co/unsloth/gemma-4-E2B-it-MLX-8bit) |

try use:

{% code overflow="wrap" %}

```bash
curl -fsSL https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/scripts/install_gemma4_mlx.sh | sh
source ~/.unsloth/unsloth_gemma4_mlx/bin/activate
python -m mlx_vlm.chat --model unsloth/gemma-4-26b-a4b-it-UD-MLX-4bit
```

{% endcode %}

## Gemma 4 Best Practices

### Prompting examples

#### Simple reasoning prompt

```
System:
<|think|>
You are a precise reasoning assistant.

User:
A train leaves at 8:15 AM and arrives at 11:47 AM. How long was the journey?
```

#### OCR / document prompt

OCR, use **high visual token budget** **560** **1120**.

```
[image first]
Extract all text from this receipt. Return line items, total, merchant, and date as JSON.
```

#### Multi-modal comparison prompt

```
[image 1]
[image 2]
Compare these two screenshots and tell me which one is more likely to confuse a new user.
```

#### Audio ASR prompt

```
[audio first]
Transcribe the following speech segment in English into English text.

Follow these specific instructions for formatting the answer:
* Only output the transcription, with no newlines.
* When transcribing numbers, write the digits, i.e. write 1.7 and not one point seven, and write 3 instead of three.
```

#### Audio translation prompt

```
[audio first]
Transcribe the following speech segment in Spanish, then translate it into English.
When formatting the answer, first output the transcription in Spanish, then one newline, then output the string 'English: ', then the translation in English.
```

### Multi-modal Settings

best results multimodal prompts, put multimodal content first:

* Put **image /audio text**.
* video, pass sequence frames first, instruction.

#### Variable image resolution

Gemma 4 supports multiple visual token budgets:

* `70`
* `140`
* `280`
* `560`
* `1120`

Use :

* **70 / 140**: classification, captioning, fast video understanding
* **280 / 560**: general multimodal chat, charts, screens, UI reasoning
* **1120**: OCR, document parsing, handwriting, small text

#### Audio video limits

* **Audio** available **E2B** **E4B**.
* Audio supports maximum **30 seconds**.
* Video supports maximum **60 seconds** assuming **1 frame per second** processing.

#### Audio prompt templates

**ASR prompt**

```
Transcribe the following speech segment in {LANGUAGE} into {LANGUAGE} text.

Follow these specific instructions for formatting the answer:
* Only output the transcription, with no newlines.
* When transcribing numbers, write the digits, i.e. write 1.7 and not one point seven, and write 3 instead of three.
```

**Speech translation prompt**

```
Transcribe the following speech segment in {SOURCE_LANGUAGE}, then translate it into {TARGET_LANGUAGE}.
When formatting the answer, first output the transcription in {SOURCE_LANGUAGE}, then one newline, then output the string '{TARGET_LANGUAGE}: ', then the translation in {TARGET_LANGUAGE}.
```

## 📊 Benchmarks

### Unsloth GGUF Benchmarks

conducted Mean KL Divergence benchmarks Gemma 4 GGUFs across providers help pick best quant (lower better).

* KL Divergence puts Unsloth GGUFs SOTA Pareto frontier
* KLD shows quantized model matches original BF16 output distribution, indicating retained accuracy.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtRVN97QDzO0Pq7SscC7x%2Fgemma%20426b%20bench.png?alt=media&#x26;token=80b4da76-efe9-4554-8e31-cca6494d456c" alt=""><figcaption><p>26B A4B - KLD benchmarks (lower better)</p></figcaption></figure></div>

### Official Gemma Benchmarks

| Gemma 4 | MMLU Pro | AIME 2026 (tools) | LiveCodeBench v6 | MMMU Pro |
| ----------- | -------: | -------------------: | ---------------: | -------: |
| **31B** | 85.2% | 89.2% | 80.0% | 76.9% |
| **26B A4B** | 82.6% | 88.3% | 77.1% | 73.8% |
| **E4B** | 69.4% | 42.5% | 52.0% | 52.6% |
| **E2B** | 60.0% | 37.5% | 44.0% | 44.2% |

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfKaFMy7LHQYNKpfsf7Zy%2Fgemma%204%20banner.png?alt=media&#x26;token=8bd8d0e0-ccb6-4ded-b99b-2c8a18370ae5" alt=""><figcaption></figcaption></figure></div>
