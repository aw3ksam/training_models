---
source_url: "https://unsloth.ai/docs/basics/finetuning-from-last-checkpoint"
title: "Finetuning from Last Checkpoint"
converted_at: "2026-04-22T05:10:55.113647"
---

# Finetuning Last Checkpoint

must edit `Trainer` first add `save_strategy` `save_steps`. saves checkpoint every 50 steps folder `outputs`.

```python
trainer = SFTTrainer(
    ....
    args = TrainingArguments(
        ....
        output_dir = "outputs",
        save_strategy = "steps",
        save_steps = 50,
    ),
)
```

trainer :

```python
trainer_stats = trainer.train(resume_from_checkpoint = True)
```

will start latest checkpoint continue training.

### Wandb Integration

```
# Install library
!pip install wandb --upgrade

# Setting up Wandb
!wandb login <token>

import os

os.environ["WANDB_PROJECT"] = "<name>"
os.environ["WANDB_LOG_MODEL"] = "checkpoint"
```

`TrainingArguments()` set

```
report_to = "wandb",
logging_steps = 1, # Change if needed
save_steps = 100 # Change if needed
run_name = "<name>" # (Optional)
```

train model, `trainer.train()`; resume training, 

```
import wandb
run = wandb.init()
artifact = run.use_artifact('<username>/<Wandb-project-name>/<run-id>', type='model')
artifact_dir = artifact.download()
trainer.train(resume_from_checkpoint=artifact_dir)
```

## :question:Early Stopping?

want stop pause finetuning / training run since evaluation loss not decreasing, can use early stopping stops training process. Use `EarlyStoppingCallback`.

usual, set trainer evaluation dataset. used stop training run `eval_loss` (evaluation loss) not decreasing 3 steps.

```python
from trl import SFTConfig, SFTTrainer
trainer = SFTTrainer(
    args = SFTConfig(
        fp16_full_eval = True,
        per_device_eval_batch_size = 2,
        eval_accumulation_steps = 4,
        output_dir = "training_checkpoints", # location of saved checkpoints for early stopping
        save_strategy = "steps",             # save model every N steps
        save_steps = 10,                     # how many steps until we save the model
        save_total_limit = 3,                # keep ony 3 saved checkpoints to save disk space
        eval_strategy = "steps",             # evaluate every N steps
        eval_steps = 10,                     # how many steps until we do evaluation
        load_best_model_at_end = True,       # MUST USE for early stopping
        metric_for_best_model = "eval_loss", # metric we want to early stop on
        greater_is_better = False,           # the lower the eval loss, the better
    ),
    model = model,
    tokenizer = tokenizer,
    train_dataset = new_dataset["train"],
    eval_dataset = new_dataset["test"],
)
```

add callback can also customized:

```python
from transformers import EarlyStoppingCallback
early_stopping_callback = EarlyStoppingCallback(
    early_stopping_patience = 3,     # How many steps we will wait if the eval loss doesn't decrease
                                     # For example the loss might increase, but decrease after 3 steps
    early_stopping_threshold = 0.0,  # Can set higher - sets how much loss should decrease by until
                                     # we consider early stopping. For eg 0.01 means if loss was
                                     # 0.02 then 0.01, we consider to early stop the run.
)
trainer.add_callback(early_stopping_callback)
```

train model usual via `trainer.train() .`
