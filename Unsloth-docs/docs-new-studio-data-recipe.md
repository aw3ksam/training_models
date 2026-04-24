---
source_url: "https://unsloth.ai/docs/new/studio/data-recipe"
title: "Unsloth Data Recipes"
converted_at: "2026-04-22T05:11:12.857568"
---

# Unsloth Data Recipes

Unsloth Studio's Data Recipes lets upload documents PDFs CSVs files transforms useable / synthetic datasets. Create edit datasets visually via graph-node workflow. guide will get started basics dive Unsloth Data Recipes.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQ6e19jESrJg0VjHnX58c%2Fdata%20recipes%20final.png?alt=media&#x26;token=8d74e453-815d-4790-83d1-76d0bc80a3ce" alt=""><figcaption></figcaption></figure></div>

### Data Recipes works

Data Recipes follows basic path. open recipes page, create pick recipe, build workflow editor, validate run preview, run full dataset output looks right. Add seed data generation blocks, validate workflow, preview sample output, run full dataset build. Unsloth Data Recipes powered **NVIDIA Nemo** [**Data Designer**](https://github.com/NVIDIA-NeMo/DataDesigner).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fc5m3JX1kUA3UwmdcJcxH%2FArea.gif?alt=media&#x26;token=33bbd908-7d6c-456a-bc58-ce495c0adca1" alt=""><figcaption><p>Example generating dataset fine-tuning model</p></figcaption></figure></div>

glance usual workflow look :

1. Open recipes page.
2. Create new recipe open existing one.
3. Add blocks define dataset workflow.
4. Click **Validate** catch configuration issues early.
5. Run preview inspect sample rows quickly.
6. Run full dataset build recipe ready.
7. Review progress output live graph **Executions** view mode details.
8. Select resulting dataset **Studio** fine tune model.

### Get Started

recipes page main entry point. Recipes stored locally browser, come back saved work later., can create blank recipe open guided learning recipe.

{% hint style="info" %}
Recipes can exported imported, easy share workflows Unsloth users :tada:. trying build specific dataset pattern, ask Unsloth Discord. Someone may already recipe can share.
{% endhint %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAwKh7speKv3eXERFhPg2%2FScreenshot%202026-03-13%20at%2008.26.11.png?alt=media&#x26;token=809ac83f-75c8-4ef2-9721-65971b3faaa5" alt="" width="563"><figcaption><p>Recipes landing page</p></figcaption></figure></div>

new concept workflows, learning recipes fastest way see seed data, prompts, expressions, validators fit together one working example. already know shape dataset want, starting empty usually quicker.

#### Choose starting path

<table><thead><tr><th>want :</th><th>Start :</th><th data-hidden></th></tr></thead><tbody><tr><td><sub><strong>Build custom workflow quickly</strong></sub></td><td><sub><strong>Start Empty</strong></sub></td><td></td></tr><tr><td><sub><strong>Learn product example</strong></sub></td><td><sub><strong>Start Learning Recipe</strong></sub></td><td></td></tr><tr><td><sub><strong>Continue previous work</strong></sub></td><td><sub><strong>Open saved recipe</strong></sub></td><td></td></tr></tbody></table>

### build editor

editor recipe takes shape. add blocks block sheet, configure dialogs, connect canvas, validate run workflow.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6A2uN85dkYAdP7v0eUyX%2Fworkflow.gif?alt=media&#x26;token=b44d9682-1825-4ddb-88f6-485a2aea3359" alt="" width="563"><figcaption><p>Example building product description workflow</p></figcaption></figure></div>

{% columns %}
{% column %}
editor core parts:

* recipe header, rename recipe switch **Editor** **Executions**
* canvas, recipe graph shown
* block sheet, add new blocks
* Configuration dialogs, define prompts, references, model aliases, validators seed settings.
* floating **Run** **Validate** controls
* need add 

{% endcolumn %}

{% column %}
common blocks reciper :

* **Seed** input data hugginface, local structured files (unstructured documents get chunked rows.
* **LLM + Models** providers, model configs, LLM generation blocks, shared tool profiles.
* **Expression** jinja2-based transforms not require LLM call.
* **Validators** filtering bad generated code built linters Python, SQL, Javascript/Typescript.
* **Samplers** deterministic columns categories subcategories.
 {% endcolumn %}
 {% endcolumns %}

### references work

blocks produce data (exceptions) becomes reference later blocks. one main ideas behind Data Recipes. create value, reuse prompts, expressions, structured outputs, validation steps.

{% hint style="info" %}
Jinja Expressions help work values arleady exist recipe. can reference nested fields `{{customer.first_name}}`, join values `{{customer.first_name}} {{customer.last_name}}` add conditional logic patterns `{% if condition %}...{% endif %}`&#x20;
{% endhint %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNJYWKeIDC6aqgT2dShsB%2FScreenshot%202026-03-13%20at%2010.06.14.png?alt=media&#x26;token=9d20bb8c-8a25-4395-9616-6429021d76f0" alt="" width="563"><figcaption><p>Example references shown editor</p></figcaption></figure></div>

example:

* category block named `domain` can references `{{ domain }}`
* seed column can used directly LLM prompt, columns seed data (eg. HF dataset columns, csv)
* structured LLM output can expose fileds later prompts
* expression block can combine earlyier values without another model call

### happens ?

Preview runs quick iteration. return sample rows analysis editor can inspect generated data commiting full run.

Full runs create persisted local dataset artifact. output later appears Studio's local dataset picker, can inspect use fine-tuning. Optionally can publish dataset hugginface repo.

### Core building blocks

{% columns %}
{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FuphMi76re2aUX7JvFNce%2FScreenshot%202026-03-13%20at%2011-35-45%20Unsloth%20Studio.png?alt=media&#x26;token=674eb5ef-5acb-4b32-ab85-11a2af2e210f" alt="" width="188"><figcaption><p>Core building blocks</p></figcaption></figure></div>
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FsdoYKdurtGeu4YgVqu0q%2FScreenshot%202026-03-13%20at%2011-38-59%20Unsloth%20Studio.png?alt=media&#x26;token=328c7ea6-591e-43fa-9e87-c71277a54736" alt="" width="188"><figcaption><p>Model LLM blocks</p></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

#### Model setup split two usable layers:

* **Model provider** defines endpoint authentifcation
* **Model Config** defines model name inference settings

setup works hosted providers, self-hosted endpoints, `vLLM`, `llama.cpp`, OpenAI-compatible API run outside Studio.

{% hint style="info" %}
Recipes not limited one model. can add multiple **Model providers** **Model config** blocks, use different models different steps, one coding another general text tasks.
{% endhint %}

model setup, can use Four LLM block types:

| Block | Output | Best |
| -------------- | ----------------- | ----------------------------------------------------------- |
| LLM Text | Free-form text | Instructions, explanations, conversations, descriptions |
| LLM Structured | JSON | Output need fixed fields predictable structure |
| LLM Code | Code | Python, SQL, Typescript code generation tasks |
| LLM Judge | Scored evaluation | Grading outputs one user-defined score |

#### Tool Profiles

{% columns %}
{% column %}
Tool profile blocks defines shared MCP based tool access one LLM blocks. Use generation step needs tools, looking code documentation `Context7`.

Image left shows Context7 MCP added configured Tool Profile block dialog:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fu4GbfrjuQyiU7cN15fDY%2FScreenshot%202026-03-13%20at%2010.50.01.png?alt=media&#x26;token=889a9425-bb40-4e41-9dab-5408b03bd3ca" alt="" width="375"><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

#### Validators

{% columns %}
{% column %}
Validor block primarly target LLM code block running generated code outputs Linter syntax validation, helps keep bad invalid code rows final dataset filtering. built-options cover Python, SQL, JavaScript/TypeScript validation.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FobyvYzcfyJkloHfHMyVC%2FScreenshot%202026-03-13%20at%2011-39-08%20Unsloth%20Studio.png?alt=media&#x26;token=19c8dbfa-c876-4f6e-9e62-5b8df515dc7b" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

### Validate, preview run

recipe workflow place, next step execution. reccomended pattern : validate first, preview quick feedback inspect generated data executions view, run full dataset feel output satisfies plan.

Use execution controls third order:

{% stepper %}
{% step %}

#### Validate

Click **Validate** catch configuration issues.
{% endstep %}

{% step %}

#### Preview

Run preview inspect sample rows analysis
{% endstep %}

{% step %}

#### Refine

Refine prompts, references, seed settings, validators.

Iterate untill feel satisfied generated data
{% endstep %}

{% step %}

#### Run full dataset build

{% endstep %}
{% endstepper %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFCcEaVt8xsaNsMFi2MoZ%2Funsloth%20chef.png?alt=media&#x26;token=0266aa36-4ba7-4364-be59-5fe57936ef7f" alt="" width="188"><figcaption></figcaption></figure>
