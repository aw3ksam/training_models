---
source_url: "https://unsloth.ai/docs/basics/faster-moe"
title: "Fine-tune MoE Models 12x Faster with Unsloth"
converted_at: "2026-04-22T05:10:54.919244"
---

# Fine-tune MoE Models 12x Faster Unsloth

’re introducing \~12x faster Mixture Experts (MoE) LLM training **>35% less VRAM** **\~6x longer context** new MoE Triton kernels new mathematical optimizations, loss accuracy.

* Unsloth now supports fast training MoE architectures including [gpt-oss](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune), [Qwen3](https://unsloth.ai/docs/models/tutorials/qwen3-how-to-run-and-fine-tune) (30B, 235B, VL, Coder), DeepSeek [R1](https://unsloth.ai/docs/models/tutorials/deepseek-r1-0528-how-to-run-locally), [V3](https://unsloth.ai/docs/models/tutorials/deepseek-v3.1-how-to-run-locally) GLM ([4.6](https://unsloth.ai/docs/models/tutorials/glm-4.6-how-to-run-locally#glm-4.6v-flash), [4.7](https://unsloth.ai/docs/models/tutorials/glm-4.7), [Flash](https://unsloth.ai/docs/models/glm-4.7-flash)).
* gpt-oss-20b fine-tunes **12.8 GB VRAM**. Qwen3-30B-A3B (16-bit LoRA) uses 63GB.
* kernels work data-center (B200, H100), **consumer** older GPUs (e.g., RTX 3090), FFT, LoRA QLoRA.

collaboration 🤗Hugging Face, made MoE training runs standardized PyTorch’s new `torch._grouped_mm` function. Transformers v5 recently optimized \~6x faster MoE v4 Unsloth pushes even custom Triton grouped‑GEMM + LoRA kernels **additional** \~2x speedup, >35% VRAM reduction >6x longer context (12-30x overall speedup vs v4).

Try Unsloth Notebooks fast MoE training:

| [**gpt-oss (20b)**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-Fine-tuning.ipynb) **(free)** | [Qwen3-30B-A3B](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_MoE.ipynb) (A100) | [GLM-4.7-Flash](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/GLM_Flash_A100\(80GB\).ipynb) (A100) |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [gpt-oss-120b](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(120B\)_A100-Fine-tuning.ipynb) (A100) | [gpt-oss (500K context)](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt_oss_\(20B\)_500K_Context_Fine_tuning.ipynb) | [TinyQwen3 MoE](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/TinyQwen3_MoE.ipynb) (test ) |

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZYAbbmao7vQbKGr7Rtiv%2Fgraph%20results%20only.png?alt=media&#x26;token=6cfb4f27-3e78-48d3-b3db-12eb4b3dcde3" alt="" width="563"><figcaption></figcaption></figure>

### 🦥 Unsloth MoE Triton Kernels

Alongside `torch._grouped_mm` (see [#what-is-torch.\_grouped\_mm](#what-is-torch._grouped_mm "mention")), created custom Triton MoE kernels can even faster cases. also **backwards compatible** older hardware A100, older PyTorch versions.

{% columns %}
{% column width="50%" %}
A100, **Triton kernels \~2.5× faster** `torch._grouped_mm`. kernels also one‑time autotune step pick best kernel config.

Auto-tuning takes \~2 minutes start training, can speed full run 35% A100 vs `_grouped_mm`, worth longer runs.
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F5COXvwLZwdY61BhFvjnI%2Funknown.png?alt=media&#x26;token=59f07dcc-cb11-47d4-bacc-ec27e7454f19" alt="" width="295"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
larger model context use, **pronounced memory savings Unsloth kernels will ** (efficiency will scale exponentially).
{% endhint %}

### :compass: Automatic backend selection

main innovation **Split LoRA approach** efficient MoE, uses \~35% less memory 2x faster training compared Transformers v5 + `torch._grouped_mm`. Custom `torch._grouped_mm` + Triton kernels \~12-30x faster Transformers v4.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKHbKsPvtiK06Uogklven%2Fnicer_training_time_vs_batch_final_tweaks6_bold.png?alt=media&#x26;token=448853ff-b760-46ad-8e9b-599c6862762b" alt="" width="563"><figcaption></figcaption></figure>

{% hint style="warning" %}
Training MoE models **4-bit** QLoRA isn’t recommended right now BitsandBytes doesn’t support. isn’t specific Unsloth. now, use bf16 LoRA full fine-tuning.
{% endhint %}

Unsloth will auto select either following backends depending hardware:

<table><thead><tr><th width="144.95001220703125">Backend</th><th>Optimizations</th></tr></thead><tbody><tr><td>grouped_mm</td><td><code>torch._grouped_mm</code> - available T4s way B200s, optimized H100s+.</td></tr><tr><td>unsloth_triton</td><td>Unsloth Triton kernels - will turn automatically A100s, older PyTorch versions.</td></tr><tr><td>native_torch</td><td>Native PyTorch. 12x slower, VRAM reductions still !</td></tr></tbody></table>

can also toggle :

```python
os.environ["UNSLOTH_MOE_BACKEND"] = "grouped_mm"
os.environ["UNSLOTH_MOE_BACKEND"] = "unsloth_triton"
os.environ["UNSLOTH_MOE_BACKEND"] = "native_torch"
```

{% hint style="success" %}
enable faster MoE training, update Unsloth via `pip install --upgrade unsloth unsloth_zoo`
{% endhint %}

### ❓torch.\_grouped\_mm?

Previously, Mixture--Experts (MoE) weights stored `ModuleList` per‑expert linear layers. practical way run forward pass ‑loop experts, expensive suboptimal.

```python
for expert_idx in expert_hit:
    expert_idx = expert_idx[0]
    if expert_idx == num_experts: continue
    _, token_idx = torch.where(expert_mask[expert_idx])
    current_state = hidden_states[token_idx]
    gate, up = nn.functional.linear(current_state, self.gate_up_proj[expert_idx]).chunk(2, dim=-1)
```

PyTorch recently introduced [`grouped_mm`](https://docs.pytorch.org/docs/main/generated/torch.nn.functional.grouped_mm.html) address exact bottleneck. parallel, provide MoE‑optimized Triton kernels. also lines key Transformers change: Transformers v5, expert weights stored [`single nn.Parameter`](https://github.com/huggingface/transformers/blob/v5.0.0/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py#L226), making `grouped_mm` natural fit faster MoE training inference.

[transformers 4.57.6](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py#L222) changed:

{% code overflow="wrap" %}

```python
self.experts = nn.ModuleList(
    [Qwen3MoeMLP(config, intermediate_size) for _ in range(self.num_experts)]
)
```

{% endcode %}

[transformers 5.0.0](https://github.com/huggingface/transformers/blob/v5.0.0/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py#L226) style:

{% code overflow="wrap" %}

```python
self.gate_up_proj = nn.Parameter(torch.empty(num_experts, 2 * intermediate_dim, hidden_dim))
```

{% endcode %}

`torch._grouped_mm` works GPUs starting NVIDIA T4, ’ve verified H100, A100, B200, RTX 6000 Pro, support broadly available.

also previously introduced Unsloth [Flex Attention](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training) gpt-oss, optimizations make even efficient.

## 📊 Kernel Results + Benchmarks

comparison across sequence lengths training speed memory usage versus Transformers v5 (already uses `torch._grouped_mm` MoE). **gpt-oss BF16 MoE training, see 7x faster training 36% VRAM reduction** NVIDIA B200. Qwen3-30B-A3B, 1.8x faster, **GLM 4.7 Flash 2.1x faster RTX PRO 6000**. benchmarks done LoRA rank = 64 LoRA modules MoE layers (gate,, ).

### gpt-oss Benchmarks

fine-tuned [unsloth/gpt-oss-20b-BF16](https://huggingface.co/unsloth/gpt-oss-20b-BF16) benchmarking. Unsloth 7x faster uses 36% less VRAM 16K context lengths. Transformers v5 + TRL goes memory whilst Unsloth not. Also speed increases sequence length case thanks [#unsloths-flex-attention-implementation](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training#unsloths-flex-attention-implementation "mention"), MoE kernels.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fja0OUMPoIM4KrWJPJyas%2Fgptoss%20new.png?alt=media&#x26;token=29205c0e-a3c9-4749-8ebc-f8125d49dcf1" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FyZkJp7w21nrlf9JfCYZ0%2Fgptoss%20graph%20only.png?alt=media&#x26;token=938e7590-b6a4-48eb-b53f-fdaa2bb2581c" alt="" width="188"><figcaption><p>Comparison transformers v4</p></figcaption></figure></div>

<table data-full-width="true"><thead><tr><th>Context Length</th><th>Unsloth (ms)</th><th>TF v5 (ms)</th><th>Unsloth Mem (GB)</th><th>TF v5 Mem (GB)</th><th>Speed </th><th>VRAM Saving</th><th data-hidden>Rank</th><th data-hidden>Unsloth Warmup (ms)</th><th data-hidden>TRL Warmup (ms)</th></tr></thead><tbody><tr><td>1024</td><td>275.35</td><td>376.99</td><td>40.91</td><td>43.88</td><td>1.4x</td><td>6.76%</td><td>8</td><td>2601.17</td><td>615.62</td></tr><tr><td>2048</td><td>292.88</td><td>696.57</td><td>41.83</td><td>44.93</td><td>2.4x</td><td>6.89%</td><td>8</td><td>4996.62</td><td>928.42</td></tr><tr><td>4096</td><td>370.30</td><td>1785.89</td><td>43.68</td><td>49.86</td><td>4.8x</td><td>12.39%</td><td>8</td><td>6648.94</td><td>2130.33</td></tr><tr><td>8192</td><td>712.33</td><td>5226.86</td><td>47.43</td><td>73.80</td><td>7.3x</td><td>35.73%</td><td>8</td><td>9632.44</td><td>5472.66</td></tr><tr><td>16384</td><td>1775.80</td><td><strong>OOM</strong></td><td>55.13</td><td><strong>OOM</strong></td><td>N/</td><td>N/</td><td>8</td><td>12696.26</td><td>N/</td></tr></tbody></table>

### Qwen3 Benchmarks

**NVIDIA B200**, see **\~1.7x speedup \~35% better memory efficiency Qwen3-30B-A3B LoRA**, memory savings improving longer sequence lengths.

Qwen3-Next Coder surprisingly fit single B200 GPU bf16 LoRA.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FonHXIql0XhGkLIDnuTfv%2Fimage.png?alt=media&#x26;token=06f97769-1d0e-4edb-b9c5-6c305376c6e8" alt="" width="563"><figcaption></figcaption></figure>

H100 GPU, perform significantly better baseline getting **1.77x speed ** training also saving \~5.3GB fine tuning 4K context length. seamlessly scale 8192 context lengths, Transformers v5 + TRL OOMs 8K. Notice use less memory 8K baseline 4K can keep pushing context length.

<table data-full-width="true"><thead><tr><th>Context Length</th><th>Unsloth (ms)</th><th>TF v5 (ms)</th><th>Unsloth Mem (GB)</th><th>TF v5 Mem (GB)</th><th>Speed </th><th>VRAM Saving</th><th data-hidden>Rank</th></tr></thead><tbody><tr><td>1024</td><td>366.3</td><td>628.3</td><td>80.88</td><td>104.80</td><td>1.7x</td><td>2.06%</td><td>8</td></tr><tr><td>2048</td><td>467.0</td><td>745.3</td><td>80.88</td><td>104.81</td><td>1.6x</td><td>2.57%</td><td>8</td></tr><tr><td>4096</td><td>711.6</td><td>975.5</td><td>80.89</td><td>104.80</td><td>1.4x</td><td>5.08%</td><td>8</td></tr><tr><td>8192</td><td>1376.6</td><td>1633.5</td><td>80.90</td><td>104.81</td><td>1.2x</td><td>9.17%</td><td>8</td></tr><tr><td>16384</td><td>3182.2</td><td>3407.9</td><td>85.53</td><td>116.61</td><td>1.1x</td><td>15.26%</td><td>8</td></tr></tbody></table>

### GLM 4.7 Benchmarks

Unsloth achieves **2.6x faster throughput >15% less VRAM** across batch sizes GLM 4.7 Flash. GLM 4.7 Flash 30B MoE (3B active parameters) agentic & coding model employs configuration similar DeepSeek MoE style, featuring 64 routed experts 1 shared expert. benchmarked Unsloth MoE training vs new optimized Transformers v5.

Use new Colab notebook GLM 4.7 Flash :

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/GLM_Flash_A100(80GB).ipynb>" %}
GLM 4.7 Flash MoE Notebook A100 80GB
{% endembed %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FbocwTistkljiMxGUA02y%2Fimage.png?alt=media&#x26;token=2a804b3a-44e4-4666-aa4f-ba6a31f69f39" alt="" width="563"><figcaption></figcaption></figure>

<table data-full-width="true"><thead><tr><th>Context Length</th><th>Unsloth (ms)</th><th>TF v5 (ms)</th><th>Unsloth Mem (GB)</th><th>TF v5 Mem (GB)</th><th>Speed </th><th>VRAM Saving</th><th data-hidden>Rank</th><th data-hidden>Unsloth Warmup (ms)</th><th data-hidden>TRL Warmup (ms)</th></tr></thead><tbody><tr><td><p></p><p>512</p></td><td>1145.0</td><td>2992.1</td><td>57.81</td><td>60.89</td><td>2.6x</td><td>6.51%</td><td>8</td><td>13317.46</td><td>893.04</td></tr><tr><td>1024</td><td>1298.9</td><td>3323.3</td><td>58.76</td><td>62.55</td><td>2.6x</td><td>6.22%</td><td>8</td><td>12895.28</td><td>937.37</td></tr><tr><td>2048</td><td>1831.9</td><td>4119.3</td><td>60.09</td><td>67.32</td><td>2.3x</td><td>9.46%</td><td>8</td><td>12531.37</td><td>1039.45</td></tr><tr><td>4096</td><td>2883.9</td><td>5646.1</td><td>63.34</td><td>76.78</td><td>2x</td><td>14.83%</td><td>8</td><td>7671.60</td><td>1643.26</td></tr></tbody></table>

### ⚡Faster LoRA MoE training

Transformers/PEFT, usual approach **merge LoRA adapter base weight** run MoE computation (especially since MoE often uses `nn.Parameter` instead `nn.Linear`). problem merge effectively **materializes LoRA delta (experts)** `lora_B @ lora_A.t`, **memory-hungry**.

Unsloth avoids. previously used idea optimize generic LoRA training inference, ’ve now applied **MoE + LoRA**. math identical, loss, gradients, outputs stay. change **order operations**, made possible matrix-multiplication associativity. reordering, get major speedups memory reductions.

{% hint style="warning" %}
Training MoE models **4-bit** QLoRA isn’t recommended right now BitsandBytes doesn’t support. isn’t specific Unsloth. now, use bf16 LoRA full fine-tuning.
{% endhint %}

optimizations **enabled default** training MoE models Unsloth (notably Qwen-3 MoE, gpt-oss, models mentioned ). can switch implementations via `UNSLOTH_MOE_BACKEND` environment variable: either `torch._grouped_mm` **Triton kernels** **basic PyTorch -loop**, depending compatibility preference. default `grouped_mm` best performance broad support.

```python
import os
# if you want to choose a different backend (grouped_mm by default), set the below variable:
# os.environ['UNSLOTH_MOE_BACKEND'] = 'unsloth_triton' # or grouped_mm or native_torch
lora_rank = 16
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "Qwen/Qwen3-30B-A3B-Instruct-2507", #MoE model
    max_seq_length = max_seq_length,
    load_in_4bit = False, # MoE nn.Parameter doesn't support bnb 4bit yet
)
model = FastLanguageModel.get_peft_model(
    model,
    r = lora_rank,
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_up_proj", "down_proj", # LoRA on MoE layers!
    ],
    lora_alpha = lora_rank*2, # *2 speeds up training
    use_gradient_checkpointing = "unsloth", # Reduces memory usage
    random_state = 3407,
)
```

## 📚 Details implementation

LoRA parameter-efficient fine-tuning method: instead updating full weight matrix, train low-rank “adapter” far fewer parameters, drastically reduces optimizer memory.

original weight shape **(m, n)**, LoRA adds two trainable matrices shapes **(m, r)** **(r, n)**. product **(m, n)**, track optimizer states gradients :

* `m*r + r*n` parameters (LoRA) instead 
* `m*n` parameters (full fine-tuning)

{% hint style="info" %}
fine-tuning MoE's - not good idea fine-tune router layer disabled default.
{% endhint %}

typical MLP layers, `m ≈ 4096, n ≈ 12k, and r ≈ 64`, ’s roughly **\~1M LoRA parameters vs \~48M full parameters -** **\~2%,** often minimal accuracy loss.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FogBmpbd8eAirmDJaDCMl%2FLoRA%20Image?alt=media&#x26;token=ce533f2c-ad6a-4cca-8588-fe0f548f8bae" alt="" width="255"><figcaption></figcaption></figure>

#### MoE LoRA changes things

MoE layers different **E expert MLPs parallel**, per‑expert change (adding LoRA) scales across experts.

Take **Qwen3‑30B‑A3B**: hidden size **m=2048**, intermediate size **n=768**, **E=128** experts **k=8** activated per token. Per expert:

* `gate_proj` `up_proj`: `(m, n) = (2048, 768)`
* `down_proj`: `(n, m) = (768, 2048)`

**LoRA rank r=64**, projection adds `r*(m+n)=64*(2048+768)=180,224` parameters per expert (≈ `11%` `2048×768` matrix). core issue `r/n = 64/768` large compared typical MLP setups, e.g., `r/n = 64/25600` [Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B/blob/main/config.json#L13) similar size.

materialize across ** experts, memory adds quickly. since `gate_proj` `up_proj` often fused `gate_up_proj`, typically materialize together, roughly doubling overhead/peak memory.

**terms memory, sequence length s, E experts `k` chosen, following common approaches**

```
# All these values are per expert
Final output: (s, n)
Input activations: (s, m)
Final output: (s, n)
```

things start diverge. peft’s approach 

```
delta = loraA@loraB  = (m,n) per expert = Emn parameters
```

Unsloth’s split LoRA approach, perform following operations

```
Y = X @ loraA : (s,m) @ (m, r)       # but sparse for k experts = ksr parameters
Y @ loraB: (s, r) @ (r, n)           # but sparse again for k experts = ksn parameters
```

Now lets take case Qwen3-30B-A3B.

`E = 128, k = 8, m = 2048, n = 768.` Plugging, get `s < 32K.`&#x20;

$$
\begin{aligned}
\text{PEFT params} &:\quad Emn \\
\text{Unsloth Split LoRA params} &:\quad ks(r+n) \\
\text{typical LoRA } &:\quad r \ll n \\
\text{Split LoRA better } &:\quad Emn > ksn ;=; Em > ks \\
\\
\text{Qwen3-30B-A3B, } \\
E &= 128, \quad k = 8, \quad m = 2048, \quad n = 768 \\
\\
\text{, Split LoRA mathematically better } \\
s &< \frac{Emn}{kn} = 32K
\end{aligned}
$$

**In terms of compute, for a sequence length `s`, `E` experts and top `k` chosen, we're doing:**

$$
\begin{aligned}
\Delta = AB,
A \in \mathbb{R}^{m \times r}, ;
B \in \mathbb{R}^{r \times n}
&\quad \Rightarrow \quad 2mnr \text{ flops per expert lora} \\
\\
W' = W + \Delta
\quad &\Rightarrow \quad mn \text{ flops} \\
\\
XW'  \quad | \quad
X \in \mathbb{R}^{s \times m}, ;
W' \in \mathbb{R}^{m \times n}
\quad &\Rightarrow \quad 2smn \text{ flops} \\
\\
\text{MoE peft lora flops}
&= E\big(2mnr + mn\big)

* 2k,smn
  \end{aligned}
  $$

In case of Unsloth split lora that we mentioned, we have

$$
\begin{aligned}
XW &= 2smn  \text{  flops} \\
Y = XA, &= 2smr
\quad \text{(applied only to routed token--expert pairs)} \\
\
Z = YB &= 2srn \\
\text{MoE split lora flops}
&= 2k\big(smn + smr + srn\big) \\
\text{Crossover condition}
&:\quad 2ksr(m+n) > 2Emn(r+1/2)
\Rightarrow
s > \frac{Emn}{k(m+n)} \times (1+ \frac{1}{2r}) \\
\\
\text{Qwen3-30B-A3B }
&:
E = 128,;
m = 2048,;
n = 768,;
k = 8 \\
\\
\Rightarrow \quad
s
& ;\approx; 16\text{K tokens}
\end{aligned}
$$

point till Split LoRA analytical perspective better `s > Emn/k(m+n)` order `16K` tokens Qwen3-30B-A3B style model.

Finally, speedups come **reduced memory traffic**: modern GPUs often **bandwidth‑bound**, transferring less data can matter FLOPs. rough speedup estimate `Emn / [k·s·(m+n)]`, depends strongly **s, E, k**, matrix shapes.

### 🔮 Model Support

Unsloth supports faster MoE training Qwen, gpt-oss, DeepSeek GLM models:

* **Qwen3** (Thinking Instruct): VL • 2507 • Coder&#x20;
* **gpt-oss**: 20B • 120B • safeguard
* **GLM**: 4.5 • 4.6 • 4.6-Air • 4.7 • 4.7-Flash
* **DeepSeek**: V3 • R1 • V3.1 • V3.2

may not uploaded MoE models, Unsloth still support.

### 📈 Benchmarks

#### gpt-oss BF16 Benchmarks

Training Speed including vs Transformers v4

<table data-full-width="false"><thead><tr><th align="right">Context length</th><th align="right">Unsloth (ms)</th><th align="right">TF v5 (ms)</th><th align="right">TF v4 (ms)</th><th align="right">Speed </th></tr></thead><tbody><tr><td align="right">1024</td><td align="right">275.35</td><td align="right">376.99</td><td align="right">2111.18</td><td align="right">1.37x</td></tr><tr><td align="right">2048</td><td align="right">292.88</td><td align="right">696.57</td><td align="right">2626.80</td><td align="right">2.38x</td></tr><tr><td align="right">4096</td><td align="right">370.30</td><td align="right">1785.89</td><td align="right">4027.93</td><td align="right">4.82x</td></tr><tr><td align="right">8192</td><td align="right">712.33</td><td align="right">5226.86</td><td align="right">8513.52</td><td align="right">7.34x</td></tr><tr><td align="right">16384</td><td align="right">1775.80</td><td align="right">OOM</td><td align="right">OOM</td><td align="right">N/</td></tr></tbody></table>

**Memory VRAM usage**

<table data-full-width="false"><thead><tr><th align="right">Context length</th><th align="right">Unsloth Mem (GB)</th><th align="right">TF v5 Mem (GB)</th><th align="right">TF v4 Mem (GB)</th><th align="right">VRAM Saving</th></tr></thead><tbody><tr><td align="right">1024</td><td align="right">40.91</td><td align="right">43.88</td><td align="right">89.75</td><td align="right">6.76%</td></tr><tr><td align="right">2048</td><td align="right">41.83</td><td align="right">44.93</td><td align="right">90.47</td><td align="right">6.89%</td></tr><tr><td align="right">4096</td><td align="right">43.68</td><td align="right">49.86</td><td align="right">92.72</td><td align="right">12.39%</td></tr><tr><td align="right">8192</td><td align="right">47.43</td><td align="right">73.80</td><td align="right">100.3</td><td align="right">35.73%</td></tr><tr><td align="right">16384</td><td align="right">55.13</td><td align="right">OOM</td><td align="right">OOM</td><td align="right">N/</td></tr></tbody></table>

## :tada: Important Unsloth Updates

1. part MoE release, also made **Gemma-3 now use Flex-Attention** default, works float16 settings (infinities solved back). **Gemma-3 now uses O(N) memory not O(N^2) memory, trains >3x faster** (scales even better context length). Previous Unsloth versions OOM.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZiM9zMhVlUaJXC4Y1REp%2Fimage.png?alt=media&#x26;token=b2f1d12e-ccdb-431c-9b65-284db3892e2c" alt="" width="375"><figcaption></figcaption></figure>

| Context | Old Peak VRAM | New Peak VRAM | VRAM Saving |
| ------- | ------------- | ------------- | ------------- |
| 1K | 20.1 GB | 20.1 GB | 0 GB (0%) |
| 2K | 21.5 GB | 21.1 GB | 0.3 GB (2%) |
| 4K | 27.7 GB | 23.3 GB | 4.5 GB (16%) |
| 8K | 52.3 GB | 27.5 GB | 24.8 GB (47%) |
| 16K | OOM | 36.0 GB | -- |
| 24K | OOM | 44.6 GB | -- |
| 32K | OOM | 53.1 GB | -- |
| 48K | OOM | 38.4 GB | -- |
| 64K | OOM | 44.7 GB | -- |

2. Vision fine-tuning now accepts mixed data images text data!
3. [Windows is now officially supported with no need for WSL](https://unsloth.ai/docs/get-started/install/windows-installation).
4. `trl==0.27.1` `transformers==5.1.0` supported - previous coverage 30% 120 notebooks, now >80% coverage - plan make 100% next days.
5. Many bug fixes updates - see <https://github.com/unslothai/unsloth/releases/tag/February-2026>

{% hint style="success" %}
enable faster MoE training, update Unsloth via `pip install --upgrade unsloth unsloth_zoo`
{% endhint %}

### Acknowledgements

thank Hugging Face team collaborating us improving MoE training community.

also sincerely thank torchao team, especially Vasily Kuznetsov (vkuzo) working helping us enabling grouped\_mm support float16 get work T4 backward compatibility A100.
