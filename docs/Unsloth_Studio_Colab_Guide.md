# Unsloth Studio in Google Colab: A Step-by-Step Guide

This guide will walk you through setting up and fine-tuning an LLM using the Unsloth Studio in Google Colab.

> **Colab Link:** [Unsloth Studio Colab Notebook](https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb)

---

## Prerequisites: Get Your Hugging Face Token
Before you begin, you will need a Hugging Face token to download base models and push your trained model back to the hub.

1. Go to Hugging Face and log in to your profile.
![Step 1](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-1.jpeg)

2. Navigate to **Settings > Access Tokens**.
3. Click **Create new token**, select **Write** permissions, and generate it. Save this token for later.
![Step 2](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-2.jpeg)

---

## Step 1: Set Up the Colab Environment
1. Open the Unsloth Studio Colab Notebook linked above.
2. Locate the **Setup: Clone repo and run setup** section. Click the **Play** button on the first cell to install the necessary dependencies.
![Step 3](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-3.jpg)
![Step 4](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-4.jpg)

3. Wait for the setup to complete. You will see an `Unsloth Studio Setup Complete` message in the output once it finishes.
![Step 5](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-5.jpg)

---

## Step 2: Launch Unsloth Studio
1. Scroll down to the **Start Unsloth Studio** section and run the cell.
![Step 6](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-6.jpg)
![Step 7](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-7.jpg)

2. The server will begin loading. Once ready, an **"Open Unsloth Studio"** button will appear in the output. Click it to launch the web interface.
![Step 8](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-8.jpg)

3. You will be greeted by an account setup screen. Enter and confirm a new password to secure your local session.
![Step 9](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-9.jpg)

---

## Step 3: Configure Your Fine-Tuning Job
1. Inside the Studio UI, click the **Train** icon on the left sidebar.
![Step 10](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-10.jpg)

2. **Configure the Model:**
   - Under Hugging Face Model, select or type the base model you want to use (e.g., `unsloth/Llama-3.2-1B`).
   - Paste your **Hugging Face Token** in the optional field.
   - Set the **Method** to your preferred fine-tuning approach (e.g., `QLoRA (4-bit)`).
![Step 11](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-11.jpg)
![Step 15](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-15.jpg)

3. **Upload Your Dataset:**
   - In the Dataset section, click **Upload**.
![Step 12](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-12.jpg)
   - Select your prepared training file (e.g., `training_data.jsonl`).
![Step 13](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-13.jpg)
![Step 14](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-14.jpg)

4. **Adjust Parameters:**
   - Review the default hyperparameters (like Max Steps, Context Length, and Learning Rate) and adjust them if necessary.

---

## Step 4: Start Training
1. Once everything is configured, click the green **Start Training** button on the right side of the screen.
![Step 16](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-16.jpg)
![Step 17](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-17.jpg)

2. The UI will automatically switch to the **Current Run** tab. Here, you can monitor the training progress in real-time, including:
   - Training Loss and Gradient Norm graphs.
   - GPU utilization, temperature, and VRAM usage.
![Step 18](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-18.jpg)

---

## Step 5: Export Your Model
1. Once the progress bar reaches 100% and training is complete, an **Export Model** button will appear next to the chat button. Click it.
![Step 19](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-19.jpg)

2. In the Export Configuration screen, select your desired **Export Method**:
   - **Merged Model**: Full 16-bit model ready for inference.
   - **LoRA Only**: Lightweight adapter files (~100 MB). Requires the base model to run.
![Step 20](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-20.jpg)
![Step 21](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-21.jpg)
   - **GGUF / Llama.cpp**: Quantized formats optimized for local runners. If you select this, choose your desired quantization level (like `Q4_K_M`).
![Step 22](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-22.jpg)

3. Click the **Export Model** button at the bottom.
![Step 23](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-23.jpg)

4. A popup will ask where to save your model:
   - **Save Locally**: Downloads the files to your Colab instance.
   - **Push to Hub**: Uploads it directly to Hugging Face. (You will need to provide your Username/Org, a Model Name, and your HF Write Token).
![Step 24](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-24.jpg)

5. Click **Start Export** to finish!
![Step 25](Unsloth_GoogleColab_Visual_Guide/asset/Unsloth_STUDIO_GoogleColab_Step-25.jpg)
