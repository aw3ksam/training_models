---
source_url: "https://unsloth.ai/docs/basics/continued-pretraining"
title: "Continued Pretraining"
converted_at: "2026-04-22T05:10:53.985402"
---

# Continued Pretraining

* [text completion notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Mistral_\(7B\)-Text_Completion.ipynb) continued pretraining/raw text.
* [continued pretraining notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Mistral_v0.3_\(7B\)-CPT.ipynb) learning another language.

can read continued pretraining release [blog post](https://unsloth.ai/blog/contpretraining).

## Continued Pretraining?

Continued continual pretraining (CPT) necessary “steer” language model understand new domains knowledge, distribution domains. Base models Llama-3 8b Mistral 7b first pretrained gigantic datasets trillions tokens (Llama-3 e.g. 15 trillion).

sometimes models not trained languages, text specific domains, law, medicine areas. continued pretraining (CPT) necessary make language model learn new tokens datasets.

## Advanced Features:

### Loading LoRA adapters continued finetuning

saved LoRA adapter Unsloth, can also continue training using LoRA weights. optimizer state will reset. load even optimizer states continue finetuning, see next section.

```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "LORA_MODEL_NAME",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
trainer = Trainer(...)
trainer.train()
```

### Continued Pretraining & Finetuning `lm_head` `embed_tokens` matrices

Add `lm_head` `embed_tokens`. Colab, sometimes will go memory Llama-3 8b., add `lm_head`.

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",
                      "lm_head", "embed_tokens",],
    lora_alpha = 16,
)
```

use 2 different learning rates - 2-10x smaller one `lm_head` `embed_tokens` :

```python
from unsloth import UnslothTrainer, UnslothTrainingArguments

trainer = UnslothTrainer(
    ....
    args = UnslothTrainingArguments(
        ....
        learning_rate = 5e-5,
        embedding_learning_rate = 5e-6, # 2-10x smaller than learning_rate
    ),
)
```
