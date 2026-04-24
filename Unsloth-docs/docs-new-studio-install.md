---
source_url: "https://unsloth.ai/docs/new/studio/install"
title: "Unsloth Studio Installation"
converted_at: "2026-04-22T05:11:13.097339"
---

# Unsloth Studio Installation

Unsloth Studio works Windows, Linux, WSL MacOS. use installation process every device, although system requirements may differ device.

<a href="#windows" class="button secondary" data-icon="windows">Windows</a><a href="#macos" class="button secondary" data-icon="apple">MacOS</a><a href="#linux-and-wsl" class="button secondary" data-icon="linux">Linux & WSL</a><a href="#docker" class="button secondary" data-icon="docker">Docker</a><a href="#developer-installation-advanced" class="button secondary" data-icon="screwdriver-wrench">Developer Install</a>

* **Mac:** CPU - [Chat](https://unsloth.ai/docs/new/chat#using-unsloth-studio-chat) + [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) works now. **MLX** training coming soon.
* **CPU: Unsloth still works without GPU**, Chat + Data Recipes.
* **Training:** Works **NVIDIA**: RTX 30, 40, 50, Blackwell, DGX Spark/Station etc. + **Intel** GPUs
* **Coming soon:** Support **Apple MLX** **AMD**.

## Install Instructions

Remember install instructions across every device:

{% stepper %}
{% step %}

#### Install Unsloth

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% hint style="success" %}
**First install now 6x faster 50% reduced size due precompiled llama.cpp binaries.**
{% endhint %}

{% hint style="info" %}
**WSL users:** will prompted `sudo` password install build dependencies (`cmake`, `git`, `libcurl4-openssl-dev`).
{% endhint %}
{% endstep %}

{% step %}

#### Launch Unsloth Studio

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fd1yMMNa65Ccz50Ke0E7r%2FScreenshot%202026-03-17%20at%2012.32.38%E2%80%AFAM.png?alt=media&#x26;token=9369cfe7-35b1-4955-b8cb-42f7ecb43780" alt="" width="375"><figcaption></figcaption></figure></div>

**open `http://localhost:8888` browser.**
{% endstep %}

{% step %}

#### Onboarding

first launch will need create password secure account sign later. ’ll see brief onboarding wizard choose model, dataset, basic settings. can skip time.
{% endstep %}

{% step %}

#### Start training running

Start fine-tuning building datasets immediately launching. See step--step guide get started Unsloth Studio:

{% content-ref url="start" %}
[start](https://unsloth.ai/docs/new/studio/start)
{% endcontent-ref %}
{% endstep %}
{% endstepper %}

### Update Unsloth Studio:

update Unsloth Studio use:

{% code overflow="wrap" %}

```bash
unsloth studio update
```

{% endcode %}

not work, can use :

#### **MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

#### **Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

## System Requirements

### <i class="fa-windows">:windows:</i> Window**s**

Unsloth Studio works directly Windows without WSL. train models, make sure system satisfies requirements:

**Requirements**

* Windows 10 Windows 11 (64-bit)
* NVIDIA GPU drivers installed
* **App Installer** (includes `winget`): [here](https://learn.microsoft.com/en-us/windows/msix/app-installer/install-update-app-installer)
* **Git**: `winget install --id Git.Git -e --source winget`
* **Python**: version 3.11, not including, 3.14
* Work inside Python environment **uv**, **venv**, **conda/mamba**

### <i class="fa-apple">:apple:</i> MacOS

Unsloth Studio works Mac devices [Chat](#run-models-locally) GGUF models [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) ([Export](https://unsloth.ai/docs/new/studio/export) coming soon). **MLX training coming soon!**

* macOS 12 Monterey newer (Intel Apple Silicon)
* Install Homebrew: [here](https://brew.sh/)
* Git: `brew install git`&#x20;
* cmake: `brew install cmake`&#x20;
* openssl: `brew install openssl`
* Python: version 3.11, not including, 3.14
* Work inside Python environment **uv**, **venv**, **conda/mamba**

### <i class="fa-linux">:linux:</i> Linux & WSL

* Ubuntu 20.04+ similar distro (64-bit)
* NVIDIA GPU drivers installed
* CUDA toolkit (12.4+ recommended, 12.8+ blackwell)
* Git: `sudo apt install git`
* Python: version 3.11, not including, 3.14
* Work inside Python environment **uv**, **venv**, **conda/mamba**

### <i class="fa-docker">:docker:</i> Docker

{% hint style="success" %}
Docker image now works Studio! working Mac compatibility.
{% endhint %}

* Pull latest Unsloth container image: `docker pull unsloth/unsloth`
* Run container via:

```bash
docker run -d -e JUPYTER_PASSWORD="mypassword" \
  -p 8888:8888 -p 8000:8000 -p 2222:22 \
  -v $(pwd)/work:/workspace/work \
  --gpus all \
  unsloth/unsloth
```

information, [see here](https://hub.docker.com/r/unsloth/unsloth#unsloth-docker-image).

* Access studio instance `http://localhost:8000` external ip address `http://external_ip_address:8000/`

### <i class="fa-microchip">:microchip:</i> CPU 

Unsloth Studio supports CPU devices [Chat](#run-models-locally) GGUF models [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) ([Export](https://unsloth.ai/docs/new/studio/export) coming soon)

* ones mentioned Linux (except NVIDIA GPU drivers) MacOS.

## Developer Installation (Advanced)

### **Install Main Repo**

#### **macOS, Linux, WSL developer installs:**

```bash
git clone https://github.com/unslothai/unsloth
cd unsloth
./install.sh --local
unsloth studio -H 0.0.0.0 -p 8888
```

#### **Windows PowerShell developer installs:**

```powershell
winget install -e --id Python.Python.3.13 --source winget
winget install --id=astral-sh.uv  -e --source winget
winget install --id Git.Git -e --source winget
git clone https://github.com/unslothai/unsloth
cd unsloth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1 --local
unsloth studio -H 0.0.0.0 -p 8888
```

### **Nightly Install**

#### **Nightly - MacOS, Linux, WSL:**

```bash
git clone https://github.com/unslothai/unsloth
cd unsloth
git checkout nightly
./install.sh --local
```

launch every time:

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

#### **Nightly - Windows:**

Run Windows Powershell:

```bash
winget install -e --id Python.Python.3.13 --source winget
winget install --id=astral-sh.uv  -e --source winget
winget install --id Git.Git -e --source winget
git clone https://github.com/unslothai/unsloth
cd unsloth
git checkout nightly
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1 --local
```

launch every time:

<pre class="language-bash"><code class="lang-bash"><strong>unsloth studio -H 0.0.0.0 -p 8888
</strong></code></pre>

### Uninstall

uninstall Unsloth Studio, follow 4 steps:

#### **1. Remove application**

* MacOS, WSL, Linux: `rm -rf ~/.unsloth/studio/unsloth ~/.unsloth/studio/studio`
* Windows (PowerShell): `Remove-Item -Recurse -Force "$HOME\.unsloth\studio\unsloth", "$HOME\.unsloth\studio\studio"`&#x20;

removes application keeps model checkpoints, exports, history, cache, chats intact.

#### **2. Remove shortcuts symlinks**

**macOS:**

```bash
rm -rf ~/Applications/Unsloth\ Studio.app ~/Desktop/Unsloth\ Studio
```

**Linux:**

```bash
rm -f ~/.local/share/applications/unsloth-studio.desktop ~/Desktop/unsloth-studio.desktop
```

**WSL / Windows (PowerShell):**

```bash
Remove-Item -Force "$HOME\Desktop\Unsloth Studio.lnk"
Remove-Item -Force "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Unsloth Studio.lnk"
```

#### **3. Remove CLI command**

**macOS, Linux, WSL:**

```bash
rm -f ~/.local/bin/unsloth
```

**Windows (PowerShell):** installer added venv's `Scripts` directory User PATH. remove, open Settings → System → → Advanced system settings → Environment Variables, find `Path` User variables, remove entry pointing `.unsloth\studio\...\Scripts`.

#### **4. Remove everything (optional)**

also delete history, cache, chats, model checkpoints, model exports, delete entire Unsloth folder:

* MacOS, WSL, Linux: `rm -rf ~/.unsloth`
* Windows (PowerShell): `Remove-Item -Recurse -Force "$HOME\.unsloth"`&#x20;

Note downloaded HF model files stored separately Hugging Face cache — none steps will remove. See **Deleting model files** want reclaim disk space.

{% hint style="warning" %}
Note: Using `rm -rf` commands will **delete everything**, including history, cache, chats etc.
{% endhint %}

### **Deleting cached HF model files**

can delete old model files either bin icon model search removing relevant cached model folder default Hugging Face cache directory. default, Hugging Face uses `~/.cache/huggingface/hub/` macOS/Linux/WSL `C:\Users\<username>\.cache\huggingface\hub\` Windows.

* **MacOS, Linux, WSL:** `~/.cache/huggingface/hub/`
* **Windows:** `%USERPROFILE%\.cache\huggingface\hub\`

`HF_HUB_CACHE` `HF_HOME` set, use location instead. Linux WSL, `XDG_CACHE_HOME` can also change default cache root.

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

**Manual instructions:** Unsloth Studio detects models downloaded Hugging Face Hub cache `(C:\Users{your_username}.cache\huggingface\hub)`. GGUF models downloaded LM Studio, note stored `C:\Users{your_username}.cache\lm-studio\models` ****** `C:\Users{your_username}\lm-studio\models`. Sometimes not visible, will need move copy.gguf files Hugging Face Hub cache directory (another path accessible llama.cpp) Unsloth Studio load.

fine-tuning model adapter Studio, can export GGUF run local inference **llama.cpp** directly Studio Chat. Unsloth Studio powered llama.cpp Hugging Face.

### <i class="fa-google">:google:</i> Google Colab notebook

’ve created [free Google Colab notebook](https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb) can explore Unsloth’s features Colab’s T4 GPUs. can train run models 22B parameters, switch larger GPU bigger models. Click 'Run ' UI pop installation.

{% columns %}
{% column %}
{% embed url="<https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb>" %}

installation complete, scroll **Start Unsloth Studio** click **Open Unsloth Studio** white box shown left:

**Scroll, see actual UI.**
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FkYitMrK55Ic6eIGqiKEJ%2FScreenshot%202026-03-16%20at%2011.21.16%E2%80%AFPM.png?alt=media&#x26;token=4388c309-a598-41f3-9301-e434c334ac1c" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% hint style="warning" %}
Sometimes Studio link may return error. happens might disabled cookies using adblocker Mozilla. can still access UI scrolling button.

Google Colab also expects stay Colab page; detects inactivity, may shut GPU session.
{% endhint %}

## Troubleshooting

<table><thead><tr><th width="211.5999755859375">Problem</th><th>Fix</th></tr></thead><tbody><tr><td>Python version error</td><td><code>sudo apt install python3.12 python3.12-venv</code> version 3.11, not including, 3.14</td></tr><tr><td><code>nvidia-smi not found</code></td><td>Install NVIDIA drivers https://www.nvidia.com/Download/index.aspx</td></tr><tr><td><code>nvcc not found</code> (CUDA)</td><td><code>sudo apt install nvidia-cuda-toolkit</code> add <code>/usr/local/cuda/bin</code> PATH</td></tr><tr><td>llama-server build failed</td><td>Non-fatal, Studio still works, GGUF inference available. Install <code>cmake</code> re-run setup fix.</td></tr><tr><td><code>cmake not found</code></td><td><code>sudo apt install cmake</code></td></tr><tr><td><code>git not found</code></td><td><code>sudo apt install git</code></td></tr><tr><td>Build failed</td><td>Delete <code>~/.unsloth/llama.cpp</code> re-run setup</td></tr></tbody></table>
