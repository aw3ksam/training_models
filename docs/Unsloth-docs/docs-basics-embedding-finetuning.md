---
source_url: "https://unsloth.ai/docs/basics/embedding-finetuning"
title: "Fine-tuning Embedding Models with Unsloth Guide"
converted_at: "2026-04-22T05:10:54.199045"
---

# Fine-tuning Embedding Models Unsloth Guide

Fine-tuning embedding models can largely improve retrieval RAG performance specific tasks. aligns model's vectors domain 'similarity' matters use case, improves search, RAG, clustering, recommendations data.

Example: headlines “Google launches Pixel 10” “Qwen releases Qwen3” might embedded similar ’re labeling 'Tech,' not similar ’re semantic search ’re different things. Fine-tuning helps model make 'right' similarity use case, reducing errors improving results.

[**Unsloth**](https://github.com/unslothai/unsloth) now supports training embedding, **classifier**, **BERT**, **reranker** models [**\~1.8-3.3x faster**](#unsloth-benchmarks) 20% less memory 2x longer context Flash Attention 2 implementations - accuracy degradation. EmbeddingGemma-300M works **3GB VRAM**. can use trained **model anywhere**: transformers, LangChain, Ollama, vLLM, llama.cpp etc.

Unsloth uses [SentenceTransformers](https://github.com/huggingface/sentence-transformers) support compatible models Qwen3-Embedding, BERT. **Even notebook upload, ’s still supported.**

**created free fine-tuning notebooks, 3 main use-cases:**

| [EmbeddingGemma (300M)](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma_\(300M\).ipynb) | [Qwen3-Embedding 4B](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_Embedding_\(4B\).ipynb) • [0.6B](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_Embedding_\(0_6B\).ipynb) | [BGE M3](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/BGE_M3.ipynb) |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [ModernBERT](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/bert_classification.ipynb) - classification | [All-MiniLM-L6-v2](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/All_MiniLM_L6_v2.ipynb) | [ModernBERT-large](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/bert_classification.ipynb) |

* `All-MiniLM-L6-v2`: produce compact, domain-specific sentence embeddings semantic search, retrieval, clustering, tuned data.
* `tomaarsen/miriad-4.4M-split`: embed medical questions biomedical papers high-quality medical semantic search RAG.
* `electroglyph/technical`: better capture meaning semantic similarity technical text (docs, specs, engineering discussions).

can view rest uploaded models [our collection here](https://huggingface.co/collections/unsloth/embedding-models).

> huge thanks Unsloth contributor [**electroglyph**](https://github.com/unslothai/unsloth/pull/3719), whose work significant support. can check electroglyph’s custom models Hugging Face [here](https://huggingface.co/electroglyph).

### 🦥 Unsloth Features

* LoRA/QLoRA full fine-tuning embeddings, without needing rewrite pipeline
* Best support encoder-`SentenceTransformer` models (`modules.json`)
* Cross-encoder models confirmed train properly even fallback path
* release also supports `transformers v5`

limited support models without `modules.json` (’ll auto-assign default `SentenceTransformers` pooling modules). ’re something custom (custom heads, nonstandard pooling), double-check outputs pooled embedding behavior.

models needed custom additions MPNet DistilBERT enabled patching gradient checkpointing `transformers` models.

### 🛠️ Fine-tuning Workflow

new fine-tuning flow centered around `FastSentenceTransformer`.

Main save/push methods:

* `save_pretrained()` Saves **LoRA adapters** local folder
* `save_pretrained_merged()` Saves **merged model** local folder
* `push_to_hub()` Pushes **LoRA adapters** Hugging Face
* `push_to_hub_merged()` Pushes **merged model** Hugging Face

**one important detail: Inference loading requires `for_inference=True`**

`from_pretrained()` similar Lacker’s fast classes, **one exception**:

* load model **inference** using `FastSentenceTransformer`, **must** pass: `for_inference=True`

inference loads look :

```python
model = FastSentenceTransformer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2",
    for_inference=True,
)
```

Hugging Face authorization, run:

```
hf auth login
```

inside virtualenv calling hub methods, :

* `push_to_hub()` `push_to_hub_merged()` **don’t require token argument**.

### ✅ Inference Deploy Anywhere! <a href="#docs-internal-guid-c10bfa80-7fff-446e-714d-732eebcd72d6" id="docs-internal-guid-c10bfa80-7fff-446e-714d-732eebcd72d6"></a>

fine-tuned Unsloth model can used deployed major tools: transformers, LangChain, Weaviate, sentence-transformers, Text Embeddings Inference (TEI), vLLM, llama.cpp, custom embedding API, pgvector, FAISS/vector databases, RAG framework.

lock fine-tuned model can later downloaded locally device.

```python
# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("<your-unsloth-finetuned-model")

query = "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]

# 2. Encode via encode_query and encode_document to automatically use the right prompts, if needed
query_embedding = model.encode_query(query)
document_embedding = model.encode_document(documents)
print(query_embedding.shape, document_embedding.shape)

# 3. Compute similarity, e.g. via the built-in similarity helper function
similarity = model.similarity(query_embedding, document_embedding)
print(similarity)
```

### 📊 Unsloth Benchmarks

Unsloth's advantages include speed embedding fine-tuning! show consistently **1.8 3.3x faster** wide variety embedding models different sequence lengths 128 2048 longer.

EmbeddingGemma-300M QLoRA works **3GB VRAM** LoRA works 6GB VRAM.

Unsloth benchmarks heatmap vs. `SentenceTransformers` + Flash Attention 2 (FA2) 4bit QLoRA. **4bit QLoRA, Unsloth 1.8x 2.6x faster:**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQqagyYR6DebgX768A0HV%2Foutput(16).png?alt=media&#x26;token=e3ea6510-b129-401a-83ae-301d01865547" alt=""><figcaption></figcaption></figure>

Unsloth benchmarks heatmap vs. `SentenceTransformers` + Flash Attention 2 (FA2) 16bit LoRA. **16bit LoRA, Unsloth 1.2x 3.3x faster:**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FTl12zuBg68ZPSyOC9hUe%2Foutput(15).png?alt=media&#x26;token=47d7cade-7eac-4366-8011-7034de087431" alt=""><figcaption></figcaption></figure>

### 🔮 Model Support

popular embedding models Unsloth supports (not models listed ):

```
Alibaba-NLP/gte-modernbert-base
BAAI/bge-large-en-v1.5
BAAI/bge-m3
BAAI/bge-reranker-v2-m3
Qwen/Qwen3-Embedding-0.6B
answerdotai/ModernBERT-base
answerdotai/ModernBERT-large
google/embeddinggemma-300m
intfloat/e5-large-v2
intfloat/multilingual-e5-large-instruct
mixedbread-ai/mxbai-embed-large-v1
sentence-transformers/all-MiniLM-L6-v2
sentence-transformers/all-mpnet-base-v2
Snowflake/snowflake-arctic-embed-l-v2.0
```

[common models](https://huggingface.co/models?library=sentence-transformers) already supported. ’s encoder-model ’d isn’t, feel free open [GitHub issue](https://github.com/unslothai/unsloth/issues) requesting.
