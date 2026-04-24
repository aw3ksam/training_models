---
source_url: "https://unsloth.ai/docs/basics/claude-code"
title: "How to Run Local LLMs with Claude Code"
converted_at: "2026-04-22T05:10:54.215377"
---

# Run Local LLMs Claude Code

step--step guide shows connect open LLMs APIs Claude Code entirely locally, complete screenshots. Run using open model Qwen3.5, DeepSeek Gemma.

tutorial, ’ll use [**Qwen3.5**](https://unsloth.ai/docs/models/qwen3.5) [GLM-4.7-Flash](https://unsloth.ai/docs/models/glm-4.7-flash). strongest 35B MoE agentic & coding model Mar 2026 (works great 24GB RAM/unified mem device) autonomously fine-tune LLM [Unsloth](https://github.com/unslothai/unsloth). can swap [any other model](https://unsloth.ai/docs/models/tutorials), update model names scripts.

<a href="#qwen3.5-tutorial" class="button secondary">Qwen3.5 Tutorial</a><a href="#glm-4.7-flash-tutorial" class="button secondary">GLM-4.7-Flash Tutorial</a><a href="#claude-code-tutorial" class="button primary" data-icon="claude">Claude Code Tutorial</a>

model quants, will utilize Unsloth [Dynamic GGUFs](https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs) run LLM quantized, retaining much accuracy possible.

{% hint style="info" %}
Claude Code changed lot since Jan 2026. lots settings necessary features will need toggle.
{% endhint %}

## 📖 LLM Setup Tutorials

begin, firstly need complete setup specific model going use. use `llama.cpp` open-source framework running LLMs Mac, Linux, Windows etc. devices. Llama.cpp contains `llama-server` allows serve deploy LLMs efficiently. model will served port 8001, agent tools routed single OpenAI-compatible endpoint.&#x20;

### Qwen3.5 Tutorial

using [Qwen3.5](https://unsloth.ai/docs/models/qwen3.5)-35B-A3B specific settings fast accurate coding tasks. enough VRAM want **smarter** model, **Qwen3.5-27B** great choice, will \~2x slower, can use Qwen3.5 variants 9B, 4B 2B.

{% hint style="info" %}
Use Qwen3.5-27B want **smarter** model enough VRAM. will \~2x slower 35B-A3B however. can use [**Qwen3-Coder-Next**](https://unsloth.ai/docs/models/qwen3-coder-next) fantastic enough VRAM.
{% endhint %}

{% stepper %}
{% step %}

#### Install llama.cpp

need install `llama.cpp` deploy/serve local LLMs use Claude Code etc. follow official build instructions correct GPU bindings maximum performance. Change `-DGGML_CUDA=ON` `-DGGML_CUDA=OFF` GPU want CPU inference. **Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` continue usual - Metal support default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev git-all -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4DmycqgjxOz6TOQd9PLJ%2Fimage.png?alt=media&#x26;token=c94db0b5-8e4a-4043-b2a3-c68bad93213e" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Download use models locally

Download model via `huggingface_hub` Python (installing via `pip install huggingface_hub hf_transfer`). use **UD-Q4\_K\_XL** quant best size/accuracy balance. can find Unsloth GGUF uploads [Collection here](https://unsloth.ai/docs/get-started/unsloth-model-catalog). downloads get stuck, see [hugging-face-hub-xet-debugging](https://unsloth.ai/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging "mention")

```bash
hf download unsloth/Qwen3.5-35B-A3B-GGUF \
    --local-dir unsloth/Qwen3.5-35B-A3B-GGUF \
    --include "*UD-Q4_K_XL*" # Use "*UD-Q2_K_XL*" for Dynamic 2bit
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRfXofrNzl1ypjfMTz15o%2Fimage.png?alt=media&#x26;token=8009de90-cd11-46ed-85b5-fca5c07b66fc" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
used `unsloth/Qwen3.5-35B-A3B-GGUF`, can use another variant 27B model `unsloth/`[`Qwen3-Coder-Next`](https://unsloth.ai/docs/models/qwen3-coder-next)`-GGUF`.
{% endhint %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxlIrQGQ0cevb1ckkSFy5%2Fimage.png?alt=media&#x26;token=b1a42562-927a-4ad2-85f8-29c2993c46aa" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Start Llama-server

deploy Qwen3.5 agentic workloads, use `llama-server`. apply [Qwen's recommended sampling parameters](https://unsloth.ai/docs/models/qwen3.5#recommended-settings) thinking mode: `temp 0.6`, `top_p 0.95`, `top-k 20`. Keep mind numbers change use non-thinking mode tasks.

Run command new terminal (use `tmux` open new terminal). **fit perfectly 24GB GPU (RTX 4090) (uses 23GB)** `--fit on` will also auto offload, see bad performance, reduce `--ctx-size`.

{% hint style="danger" %}
used `--cache-type-k q8_0 --cache-type-v q8_0` KV cache quantization less VRAM usage. full precision, use `--cache-type-k bf16 --cache-type-v bf16` According multiple reports, Qwen3.5 degrades accuracy `f16` KV cache, not use `--cache-type-k f16 --cache-type-v f16` also default llama.cpp. Note bf16 KV Cache might slightly slower machines.
{% endhint %}

```bash
./llama.cpp/llama-server \
    --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf \
    --alias "unsloth/Qwen3.5-35B-A3B" \
    --temp 0.6 \
    --top-p 0.95 \
    --top-k 20 \
    --min-p 0.00 \
    --port 8001 \
    --kv-unified \
    --cache-type-k q8_0 --cache-type-v q8_0 \
    --flash-attn on --fit on \
    --ctx-size 131072 # change as required
```

{% hint style="success" %}
can also disable thinking Qwen3.5 can improve performance agentic coding stuff. disable thinking llama.cpp add llama-server command:

`--chat-template-kwargs "{\"enable_thinking\": false}"`

<img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F373wtRRbMcobtjV5e6xf%2Fkerkekke.png?alt=media&#x26;token=2cd3b8c7-93b6-41cb-8bce-41f1aee819eb" alt="" data-size="original">
{% endhint %}
{% endstep %}
{% endstepper %}

### GLM-4.7-Flash Tutorial

{% stepper %}
{% step %}

#### Install llama.cpp

need install `llama.cpp` deploy/serve local LLMs use Claude Code etc. follow official build instructions correct GPU bindings maximum performance. Change `-DGGML_CUDA=ON` `-DGGML_CUDA=OFF` GPU want CPU inference. **Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` continue usual - Metal support default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev git-all -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4DmycqgjxOz6TOQd9PLJ%2Fimage.png?alt=media&#x26;token=c94db0b5-8e4a-4043-b2a3-c68bad93213e" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Download use models locally

Download model via `huggingface_hub` Python (installing via `pip install huggingface_hub hf_transfer`). use **UD-Q4\_K\_XL** quant best size/accuracy balance. can find Unsloth GGUF uploads [Collection here](https://unsloth.ai/docs/get-started/unsloth-model-catalog). downloads get stuck, see [hugging-face-hub-xet-debugging](https://unsloth.ai/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging "mention")

{% hint style="success" %}
used `unsloth/GLM-4.7-Flash-GGUF`, can use anything `unsloth/Qwen3-Coder-Next-GGUF` - see [qwen3-coder-next](https://unsloth.ai/docs/models/qwen3-coder-next "mention")
{% endhint %}

```python
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id = "unsloth/GLM-4.7-Flash-GGUF",
    local_dir = "unsloth/GLM-4.7-Flash-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxlIrQGQ0cevb1ckkSFy5%2Fimage.png?alt=media&#x26;token=b1a42562-927a-4ad2-85f8-29c2993c46aa" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Start Llama-server

deploy GLM-4.7-Flash agentic workloads, use `llama-server`. apply Z.ai's recommended sampling parameters (`temp 1.0`, `top_p 0.95`).

Run command new terminal (use `tmux` open new terminal). **fit perfectly 24GB GPU (RTX 4090) (uses 23GB)** `--fit on` will also auto offload, see bad performance, reduce `--ctx-size`.

{% hint style="danger" %}
used `--cache-type-k q8_0 --cache-type-v q8_0` KV cache quantization reduce VRAM usage. see reduced quality, instead can use `bf16` will increase VRAM use twice: `--cache-type-k bf16 --cache-type-v bf16`
{% endhint %}

```bash
./llama.cpp/llama-server \
    --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q4_K_XL.gguf \
    --alias "unsloth/GLM-4.7-Flash" \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --port 8001 \
    --kv-unified \
    --cache-type-k q8_0 --cache-type-v q8_0 \
    --flash-attn on --fit on \
    --batch-size 4096 --ubatch-size 1024 \
    --ctx-size 131072 #change as required
```

{% hint style="success" %}
can also disable thinking GLM-4.7-Flash can improve performance agentic coding stuff. disable thinking llama.cpp add llama-server command:

`--chat-template-kwargs "{\"enable_thinking\": false}"`

<img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FyKf6guCV8snRaAV16Zxc%2FG_16XLgXUAEnSWH.jpg?alt=media&#x26;token=3b557c6d-3f6f-4515-ba9f-4cc8b50bcef1" alt="" data-size="original">
{% endhint %}
{% endstep %}
{% endstepper %}

## <i class="fa-claude">:claude:</i> Claude Code Tutorial

{% hint style="danger" %}
See [#fixing-90-slower-inference-in-claude-code](#fixing-90-slower-inference-in-claude-code "mention") installing Claude Code fix open models 90% slower due KV Cache invalidation.
{% endhint %}

done first steps setting local LLM, time setup Claude Code. Claude Code Anthropic's agentic coding tool lives terminal, understands codebase, handles complex Git workflows via natural language.

#### **Install Claude Code run locally**

{% tabs %}
{% tab title="Mac / Linux Setups" %}

```bash
curl -fsSL https://claude.ai/install.sh | bash
# Or via Homebrew: brew install --cask claude-code
```

**Configure**

Set `ANTHROPIC_BASE_URL` environment variable redirect Claude Code local `llama.cpp` server.

```bash
export ANTHROPIC_BASE_URL="http://localhost:8001"
```

Also might need set `ANTHROPIC_API_KEY` depending server. example:

```bash
export ANTHROPIC_API_KEY='sk-no-key-required' ## or 'sk-1234'
```

**Session vs Persistent:** commands apply current terminal. persist across new terminals:

Add `export` line `~/.bashrc` (bash) `~/.zshrc` (zsh).

{% hint style="warning" %}
see `Unable to connect to API (ConnectionRefused)`, remember unset `ANTHROPIC_BASE_URL` via `unset ANTHROPIC_BASE_URL`
{% endhint %}

**Missing API key**

see, set `export ANTHROPIC_API_KEY='sk-no-key-required' ## or 'sk-1234'`

{% hint style="info" %}
Claude Code still asks sign first run, add `"hasCompletedOnboarding": true` `"primaryApiKey": "sk-dummy-key"` `~/.claude.json`. VS Code extension, also enable **Disable Login Prompt** settings (add `"claudeCode.disableLoginPrompt": true` `settings.json`).
{% endhint %}
{% endtab %}

{% tab title="Windows Setups" %}
Use Powershell commands :

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Configure**

Set `ANTHROPIC_BASE_URL` environment variable redirect Claude Code local `llama.cpp` server. Also must use `$env:CLAUDE_CODE_ATTRIBUTION_HEADER=0` see.

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:8001"
```

{% hint style="danger" %}
Claude Code recently prepends changes Claude Code Attribution header, invalidates KV Cache. See [LocalLlama discussion](https://www.reddit.com/r/LocalLLaMA/comments/1r47fz0/claude_code_with_local_models_full_prompt/).

solve, `$env:CLAUDE_CODE_ATTRIBUTION_HEADER=0` edit `~/.claude/settings.json` :

```
{
    ...
    "env": {
        "CLAUDE_CODE_ATTRIBUTION_HEADER" : "0",
        ...
    }
}
```

{% endhint %}

**Session vs Persistent:** commands apply current terminal. persist across new terminals:

Run `setx ANTHROPIC_BASE_URL "http://localhost:8001"`, add `$env:` line `$PROFILE`.

{% hint style="info" %}
Claude Code still asks sign first run, add `"hasCompletedOnboarding": true` `"primaryApiKey": "sk-dummy-key"` `~/.claude.json`. VS Code extension, also enable **Disable Login Prompt** settings (add `"claudeCode.disableLoginPrompt": true` `settings.json`).
{% endhint %}
{% endtab %}
{% endtabs %}

### :detective:Fixing 90% slower inference Claude Code

{% hint style="danger" %}
Claude Code recently prepends adds Claude Code Attribution header, **invalidates KV Cache, making inference 90% slower local models**. See [LocalLlama discussion](https://www.reddit.com/r/LocalLLaMA/comments/1r47fz0/claude_code_with_local_models_full_prompt/).
{% endhint %}

solve, edit `~/.claude/settings.json` include `CLAUDE_CODE_ATTRIBUTION_HEADER` set 0 within `"env"`

{% hint style="info" %}
Using `export CLAUDE_CODE_ATTRIBUTION_HEADER=0` **NOT** work!
{% endhint %}

example `cat > ~/.claude/settings.json` add (pasted, ENTER CTRL+D save ). previous `~/.claude/settings.json` file, add `"CLAUDE_CODE_ATTRIBUTION_HEADER" : "0"` "env" section, leave rest settings file unchanged.

<pre><code>{
 "promptSuggestionEnabled": false,
 "env": {
 "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
 "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
 <a data-footnote-ref href="#user-content-fn-1">"CLAUDE_CODE_ATTRIBUTION_HEADER" : "0"</a>
 },
 "attribution": {
 "commit": "",
 "pr": ""
 },
 "plansDirectory" : "./plans",
 "prefersReducedMotion" : true,
 "terminalProgressBarEnabled" : false,
 "effortLevel" : "high"
}
</code></pre>

#### :star2:Running Claude Code locally Linux / Mac / Windows

{% hint style="success" %}
used `unsloth/GLM-4.7-Flash-GGUF`, can use anything `unsloth/Qwen3.5-35B-A3B-GGUF`.
{% endhint %}

{% hint style="danger" %}
See [#fixing-90-slower-inference-in-claude-code](#fixing-90-slower-inference-in-claude-code "mention") first fix open models 90% slower due KV Cache invalidation.
{% endhint %}

Navigate project folder (`mkdir project ; cd project`) run:

```bash
claude --model unsloth/GLM-4.7-Flash
```

use Qwen3.5-35B-A3B, change :

```bash
claude --model unsloth/Qwen3.5-35B-A3B
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fnyc5BnXQiXPRZnyuYZt3%2Fimage.png?alt=media&#x26;token=72011cb6-abed-4a41-99b0-104ef5d0111f" alt=""><figcaption></figcaption></figure>

set Claude Code execute commands without approvals **(BEWARE will make Claude Code execute code however likes without approvals!)**

{% code overflow="wrap" %}

```bash
claude --model unsloth/GLM-4.7-Flash --dangerously-skip-permissions
```

{% endcode %}

Try prompt install run simple Unsloth finetune:

{% code overflow="wrap" %}

```
You can only work in the cwd project/. Do not search for CLAUDE.md - this is it. Install Unsloth via a virtual environment via uv. Use `python -m venv unsloth_env` then `source unsloth_env/bin/activate` if possible. See https://unsloth.ai/docs/get-started/install/pip-install on how (get it and read). Then do a simple Unsloth finetuning run described in https://github.com/unslothai/unsloth. You have access to 1 GPU.
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBkpEsVssYZG9wHvvWMRH%2Fimage.png?alt=media&#x26;token=e1a8283f-49ed-4b78-8052-d8970f069d5b" alt=""><figcaption></figcaption></figure>

waiting bit, Unsloth will installed venv via uv, loaded :

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHATFwDrR1gP44XFbzWcv%2Fimage.png?alt=media&#x26;token=6ff63733-686d-4b08-bdd5-66a6fa4aa34c" alt=""><figcaption></figcaption></figure>

finally will see successfully finetuned model Unsloth!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZjQ6askaixcYOMrr2qMi%2Fimage.png?alt=media&#x26;token=e0e0047d-b6a2-421f-a86b-68e093a3a17a" alt=""><figcaption></figcaption></figure>

**IDE Extension (VS Code / Cursor)**

can also use Claude Code directly inside editor via official extension:

* [Install for VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
* [Install for Cursor](cursor:extension/anthropic.claude-code)
* [Claude Code in VS Code docs](https://code.claude.com/docs/en/vs-code)

Alternatively, press `Ctrl+Shift+X` (Windows/Linux) `Cmd+Shift+X` (Mac), search **Claude Code**, click **Install**.

{% hint style="warning" %}
see `Unable to connect to API (ConnectionRefused)`, remember unset `ANTHROPIC_BASE_URL` via `unset ANTHROPIC_BASE_URL`
{% endhint %}

{% hint style="danger" %}
find open models 90% slower, see [#claude-code-90-slower-inference](#claude-code-90-slower-inference "mention") first fix KV cache invalidated.
{% endhint %}

[^1]: Must use !
