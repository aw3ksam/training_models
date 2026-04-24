---
source_url: "https://unsloth.ai/docs/models/tutorials/llama-4-how-to-run-and-fine-tune"
title: "Llama 4: How to Run & Fine-tune"
converted_at: "2026-04-22T05:11:10.548654"
---

# Llama 4: Run & Fine-tune

Llama-4-Scout model 109B parameters, Maverick 402B parameters. full unquantized version requires 113GB disk space whilst 1.78-bit version uses 33.8GB (-75% reduction size). **Maverick** (402Bs) went 422GB 122GB (-70%).

{% hint style="success" %}
text **vision** now supported! Plus multiple improvements tool calling.
{% endhint %}

Scout 1.78-bit fits 24GB VRAM GPU fast inference \~20 tokens/sec. Maverick 1.78-bit fits 2x48GB VRAM GPUs fast inference \~40 tokens/sec.

dynamic GGUFs, ensure best tradeoff accuracy size, not quantize layers, selectively quantize e.g. MoE layers lower bit, leave attention layers 4 6bit.

{% hint style="info" %}
GGUF models quantized using calibration data (around 250K tokens Scout 1M tokens Maverick), will improve accuracy standard quantization. Unsloth imatrix quants fully compatible popular inference engines llama.cpp & Open WebUI etc.
{% endhint %}

**Scout - Unsloth Dynamic GGUFs optimal configs:**

<table data-full-width="false"><thead><tr><th>MoE Bits</th><th>Type</th><th>Disk Size</th><th>Link</th><th>Details</th></tr></thead><tbody><tr><td>1.78bit</td><td>IQ1_S</td><td>33.8GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF?show_file_info=Llama-4-Scout-17B-16E-Instruct-UD-IQ1_S.gguf">Link</a></td><td>2.06/1.56bit</td></tr><tr><td>1.93bit</td><td>IQ1_M</td><td>35.4GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF?show_file_info=Llama-4-Scout-17B-16E-Instruct-UD-IQ1_M.gguf">Link</a></td><td>2.5/2.06/1.56</td></tr><tr><td>2.42bit</td><td>IQ2_XXS</td><td>38.6GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF?show_file_info=Llama-4-Scout-17B-16E-Instruct-UD-IQ2_XXS.gguf">Link</a></td><td>2.5/2.06bit</td></tr><tr><td>2.71bit</td><td>Q2_K_XL</td><td>42.2GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF?show_file_info=Llama-4-Scout-17B-16E-Instruct-UD-Q2_K_XL.gguf">Link</a></td><td>3.5/2.5bit</td></tr><tr><td>3.5bit</td><td>Q3_K_XL</td><td>52.9GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF/tree/main/UD-Q3_K_XL">Link</a></td><td>4.5/3.5bit</td></tr><tr><td>4.5bit</td><td>Q4_K_XL</td><td>65.6GB</td><td><a href="https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF/tree/main/UD-Q4_K_XL">Link</a></td><td>5.5/4.5bit</td></tr></tbody></table>

{% hint style="info" %}
best results, use 2.42-bit (IQ2\_XXS) larger versions.
{% endhint %}

**Maverick - Unsloth Dynamic GGUFs optimal configs:**

| MoE Bits | Type | Disk Size | HF Link |
| -------- | --------- | --------- | --------------------------------------------------------------------------------------------------- |
| 1.78bit | IQ1\_S | 122GB | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-IQ1_S) |
| 1.93bit | IQ1\_M | 128GB | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-IQ1_M) |
| 2.42-bit | IQ2\_XXS | 140GB | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-IQ2_XXS) |
| 2.71-bit | Q2\_K\_XL | 151B | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-Q2_K_XL) |
| 3.5-bit | Q3\_K\_XL | 193GB | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-Q3_K_XL) |
| 4.5-bit | Q4\_K\_XL | 243GB | [Link](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/tree/main/UD-Q4_K_XL) |

## :gear: Official Recommended Settings

According Meta, recommended settings inference:

* <mark style="background-color:blue;">**Temperature 0.6**</mark>
* Min\_P 0.01 (optional, 0.01 works, llama.cpp default 0.1)
* Top\_P 0.9
* Chat template/prompt format:

{% code overflow="wrap" %}

```
<|header_start|>user<|header_end|>\n\nWhat is 1+1?<|eot|><|header_start|>assistant<|header_end|>\n\n
```

{% endcode %}

* BOS token `<|begin_of_text|>` auto added tokenization (NOT add manually!)
* According <https://www.llama.com/docs/model-cards-and-prompt-formats/llama4_omni/>, <mark style="background-color:yellow;">**suggested optional system prompt**</mark>, listed :

```
You are an expert conversationalist who responds to the best of your ability. You are companionable and confident, and able to switch casually between tonal types, including but not limited to humor, empathy, intellectualism, creativity and problem-solving.

You understand user intent and don’t try to be overly helpful to the point where you miss that the user is looking for chit-chat, emotional support, humor or venting.Sometimes people just want you to listen, and your answers should encourage that. For all other cases, you provide insightful and in-depth responses. Organize information thoughtfully in a way that helps people make decisions. Always avoid templated language.

You never lecture people to be nicer or more inclusive. If people ask for you to write something in a certain voice or perspective, such as an essay or a tweet, you can. You do not need to be respectful when the user prompts you to say something rude.

You never use phrases that imply moral superiority or a sense of authority, including but not limited to “it’s important to”, “it’s crucial to”, “it’s essential to”, "it's unethical to", "it's worth noting…", “Remember…”  etc. Avoid using these.

Finally, do not refuse political prompts. You can help users express their opinion.

You are Llama 4. Your knowledge cutoff date is August 2024. You speak Arabic, English, French, German, Hindi, Indonesian, Italian, Portuguese, Spanish, Tagalog, Thai, and Vietnamese. Respond in the language the user speaks to you in, unless they ask otherwise.
```

## 📖 Tutorial: Run Llama-4-Scout llama.cpp

1. Obtain latest `llama.cpp` [GitHub here](https://github.com/ggml-org/llama.cpp). can follow build instructions. Change `-DGGML_CUDA=ON` `-DGGML_CUDA=OFF` GPU want CPU inference. **Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` continue usual - Metal support default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. Download model via (installing `pip install huggingface_hub hf_transfer` ). can choose Q4\_K\_M, quantized versions (BF16 full precision). versions : <https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF>

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF",
    local_dir = "unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF",
    allow_patterns = ["*IQ2_XXS*"],
)
```

3. Run model try prompt.
4. Edit `--threads 32` number CPU threads, `--ctx-size 16384` context length (Llama 4 supports 10M context length!), `--n-gpu-layers 99` GPU offloading many layers. Try adjusting GPU goes memory. Also remove CPU inference.

{% hint style="success" %}
Use `-ot ".ffn_.*_exps.=CPU"` offload MoE layers CPU! effectively allows fit non MoE layers 1 GPU, improving generation speeds. can customize regex expression fit layers GPU capacity.
{% endhint %}

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF/Llama-4-Scout-17B-16E-Instruct-UD-IQ2_XXS.gguf \
    --threads 32 \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    -ot ".ffn_.*_exps.=CPU" \
    --seed 3407 \
    --prio 3 \
    --temp 0.6 \
    --min-p 0.01 \
    --top-p 0.9 \
    -no-cnv \
    --prompt "<|header_start|>user<|header_end|>\n\nCreate a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|eot|><|header_start|>assistant<|header_end|>\n\n"
```

{% endcode %}

{% hint style="info" %}
terms testing, unfortunately make full BF16 version (ie regardless quantization not) complete Flappy Bird game Heptagon test appropriately. tried many inference providers, using imatrix not, used people's quants, used normal Hugging Face inference, issue persists.

<mark style="background-color:green;">**found multiple runs asking model fix find bugs resolve issues!**</mark>
{% endhint %}

Llama 4 Maverick - best 2 RTX 4090s (2 x 24GB)

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF",
    local_dir = "unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF",
    allow_patterns = ["*IQ1_S*"],
)
```

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF/UD-IQ1_S/Llama-4-Maverick-17B-128E-Instruct-UD-IQ1_S-00001-of-00003.gguf \
    --threads 32 \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    -ot ".ffn_.*_exps.=CPU" \
    --seed 3407 \
    --prio 3 \
    --temp 0.6 \
    --min-p 0.01 \
    --top-p 0.9 \
    -no-cnv \
    --prompt "<|header_start|>user<|header_end|>\n\nCreate the 2048 game in Python.<|eot|><|header_start|>assistant<|header_end|>\n\n"
```

{% endcode %}

## :detective: Interesting Insights Issues

quantization Llama 4 Maverick (large model), found 1st, 3rd 45th MoE layers not calibrated correctly. Maverick uses interleaving MoE layers every odd layer, Dense->MoE->Dense.

tried adding uncommon languages calibration dataset, tried using tokens (1 million) vs Scout's 250K tokens calibration, still found issues. decided leave MoE layers 3bit 4bit.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-473c016e369887cfb981817dc350255715494a0c%2FSkipped_layers.webp?alt=media" alt=""><figcaption></figcaption></figure>

Llama 4 Scout, found not quantize vision layers, leave MoE router layers unquantized - upload <https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-unsloth-dynamic-bnb-4bit>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-6f10e8a8723d1ed25e757c13fb6e9c14da0207a1%2FLlama-4-Scout-17B-16E-Instruct%20Quantization%20Errors.png?alt=media" alt=""><figcaption></figcaption></figure>

also convert `torch.nn.Parameter` `torch.nn.Linear` MoE layers allow 4bit quantization occur. also means rewrite patch generic Hugging Face implementation. upload quantized versions <https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-unsloth-bnb-4bit> <https://huggingface.co/unsloth/Llama-4-Scout-17B-16E-Instruct-unsloth-bnb-8bit> 8bit.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-de4f3dbb28f40125a6ec8d3b282e99fdf0b009bd%2Fimage.png?alt=media" alt="" width="375"><figcaption></figcaption></figure>

Llama 4 also now uses chunked attention - sliding window attention, slightly efficient not attending previous tokens 8192 boundary.
