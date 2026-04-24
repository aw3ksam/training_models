# **Preprocess**

In addition to loading datasets, 🤗 Datasets' main goal is to offer a diverse set of preprocessing functions to get a dataset into an appropriate format for training with your machine learning framework.  
Depending on your dataset modality, you will likely need to:

* **Tokenize** a text dataset.  
* **Resample** an audio dataset.  
* **Apply transforms** to an image dataset.

The final step is usually setting the dataset format to be compatible with your machine learning framework.

Bash

pip install transformers

## ---

**Tokenize text**

Models cannot process raw text; it must be converted into numbers via tokenization.

1. **Load data and tokenizer**:  
   Python  
   from transformers import AutoTokenizer  
   from datasets import load\_dataset

   tokenizer \= AutoTokenizer.from\_pretrained("bert-base-uncased")  
   dataset \= load\_dataset("cornell-movie-review-data/rotten\_tomatoes", split="train")

2. **Tokenize the entire dataset**: Use map() with batched=True for speed.  
   Python  
   def tokenization(example):  
       return tokenizer(example\["text"\])

   dataset \= dataset.map(tokenization, batched=True)

3. **Set Format**:  
   * **PyTorch**:  
     Python  
     dataset.set\_format(type="torch", columns=\["input\_ids", "token\_type\_ids", "attention\_mask", "label"\])

   * **TensorFlow**:  
     Python  
     from transformers import DataCollatorWithPadding  
     data\_collator \= DataCollatorWithPadding(tokenizer=tokenizer, return\_tensors="tf")  
     tf\_dataset \= dataset.to\_tf\_dataset(  
         columns=\["input\_ids", "token\_type\_ids", "attention\_mask"\],  
         label\_cols=\["label"\],  
         batch\_size=2,  
         collate\_fn=data\_collator,  
         shuffle=True  
     )

## ---

**Resample audio signals**

It is critical that the sampling rate of your dataset matches the rate used to pretrain your model (e.g., Wav2Vec2 uses 16kHz).

1. **Load data and feature extractor**:  
   Python  
   from transformers import AutoFeatureExtractor  
   from datasets import load\_dataset, Audio

   feature\_extractor \= AutoFeatureExtractor.from\_pretrained("facebook/wav2vec2-base-960h")  
   dataset \= load\_dataset("PolyAI/minds14", "en-US", split="train")

2. **Resample**: Use cast\_column to upsample or downsample.  
   Python  
   dataset \= dataset.cast\_column("audio", Audio(sampling\_rate=16\_000))

3. **Preprocess**:  
   Python  
   def preprocess\_function(examples):  
       audio\_arrays \= \[x.get\_all\_samples().data for x in examples\["audio"\]\]  
       return feature\_extractor(audio\_arrays, sampling\_rate=16000, max\_length=16000, truncation=True)

   dataset \= dataset.map(preprocess\_function, batched=True)

## ---

**Apply data augmentations (Images)**

Data augmentation introduces random variations to images (color jitter, cropping, etc.) without changing the label.

1. **Setup**:  
   Python  
   from transformers import AutoFeatureExtractor  
   from datasets import load\_dataset, Image

   dataset \= load\_dataset("AI-Lab-Makerere/beans", split="train")  
   dataset \= dataset.cast\_column("image", Image(mode="RGB"))

2. **Albumentations Pipeline**:  
   Python  
   import albumentations as A  
   import numpy as np  
   from PIL import Image

   transform \= A.Compose(\[  
       A.RandomCrop(height=256, width=256, pad\_if\_needed=True, p=1),  
       A.HorizontalFlip(p=0.5),  
       A.ColorJitter(p=0.5)  
   \])

3. **Apply Transform**:  
   Python  
   def albumentations\_transforms(examples):  
       transformed\_images \= \[\]  
       for image in examples\["image"\]:  
           image\_np \= np.array(image.convert("RGB"))  
           transformed\_image \= transform(image=image\_np)\["image"\]  
           transformed\_images.append(Image.fromarray(transformed\_image))  
       examples\["pixel\_values"\] \= transformed\_images  
       return examples

   dataset \= dataset.with\_transform(albumentations\_transforms)

**Sources**  
1\. [https://huggingface.co/docs/datasets/use\_dataset](https://huggingface.co/docs/datasets/use_dataset)  
2\. [https://huggingface.co/docs/datasets/use\_dataset](https://huggingface.co/docs/datasets/use_dataset)  
3\. [https://huggingface.co/docs/datasets/use\_dataset](https://huggingface.co/docs/datasets/use_dataset)  
4\. [https://huggingface.co/docs/datasets/use\_dataset](https://huggingface.co/docs/datasets/use_dataset)  
5\. [https://erhwenkuo.github.io/huggingface/datasets/tutorial/use\_dataset/](https://erhwenkuo.github.io/huggingface/datasets/tutorial/use_dataset/)