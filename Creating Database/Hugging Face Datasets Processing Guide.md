# **Process**

🤗 Datasets provides many tools for modifying the structure and content of a dataset. These tools are important for tidying up a dataset, creating additional columns, converting between features and formats, and much more.

This guide will show you how to:

* Reorder rows and split the dataset.

* Rename and remove columns, and other common column operations.

* Apply processing functions to each example in a dataset.

* Concatenate datasets.

* Apply a custom formatting transform.

* Save and export processed datasets.

The examples in this guide use the MRPC dataset:

Python

from datasets import load\_dataset  
dataset \= load\_dataset("nyu-mll/glue", "mrpc", split="train")

\[\!NOTE\]  
All processing methods in this guide return a new Dataset object. Modification is not done in-place.

## ---

**Sort, shuffle, select, split, and shard**

### **Sort**

Use sort() to sort column values according to their numerical values. The provided column must be NumPy compatible.

Python

\>\>\> dataset\["label"\]\[:10\]  
\[1, 0, 1, 0, 1, 1, 0, 1, 0, 0\]  
\>\>\> sorted\_dataset \= dataset.sort("label")  
\>\>\> sorted\_dataset\["label"\]\[:10\]  
\[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\]

### **Shuffle**

The shuffle() function randomly rearranges the column values.

Python

\>\>\> shuffled\_dataset \= sorted\_dataset.shuffle(seed=42)  
\>\>\> shuffled\_dataset\["label"\]\[:10\]  
\[1, 1, 1, 0, 1, 1, 1, 1, 1, 0\]

### **Select and Filter**

* **select()**: Returns rows according to a list of indices.  
* **filter()**: Returns rows that match a specified condition.

Python

\# Select  
\>\>\> small\_dataset \= dataset.select(\[0, 10, 20, 30, 40, 50\])

\# Filter  
\>\>\> start\_with\_ar \= dataset.filter(lambda example: example\["sentence1"\].startswith("Ar"))

### **Split**

The train\_test\_split() function creates train and test splits if your dataset doesn't already have them.

Python

\>\>\> dataset.train\_test\_split(test\_size=0.1)  
{'train': Dataset(...), 'test': Dataset(...)}

### **Shard**

Use shard() to divide a very large dataset into a predefined number of chunks.

Python

\>\>\> dataset.shard(num\_shards=4, index=0)

## ---

**Rename, remove, cast, and flatten**

### **Rename**

Use rename\_column() to change a column name.

Python

\>\>\> dataset \= dataset.rename\_column("sentence1", "sentenceA")

### **Remove**

Use remove\_columns() to drop one or more columns.

Python

\>\>\> dataset \= dataset.remove\_columns(\["label", "idx"\])

### **Cast**

The cast() function transforms the feature type of one or more columns (e.g., changing ClassLabel names).

Python

\>\>\> from datasets import ClassLabel  
\>\>\> new\_features \= dataset.features.copy()  
\>\>\> new\_features\["label"\] \= ClassLabel(names=\["negative", "positive"\])  
\>\>\> dataset \= dataset.cast(new\_features)

### **Flatten**

Use flatten() to extract subfields from a nested structure (like SQuAD's answers) into separate columns.

Python

\>\>\> flat\_dataset \= dataset.flatten()

## ---

**Map**

The map() function is used to apply a processing function to each example in a dataset, independently or in batches.

Python

\>\>\> def add\_prefix(example):  
...     example\["sentence1"\] \= 'My sentence: ' \+ example\["sentence1"\]  
...     return example

\>\>\> updated\_dataset \= dataset.map(add\_prefix)

### **Data Augmentation**

map() can also be used for data augmentation, such as generating alternative words for masked tokens.

### **Batching**

Setting batched=True allows the function to accept a batch of examples, which is significantly faster for many operations (like tokenization).

Python

\>\>\> encoded\_dataset \= dataset.map(lambda examples: tokenizer(examples\["sentence1"\]), batched=True)

## ---

**Save and Export**

### **Save**

You can save a dataset to the Hugging Face Hub or locally on disk.

* **Hub:** dataset.push\_to\_hub("username/my\_dataset")  
* **Disk:** dataset.save\_to\_disk("path/of/directory")

### **Export**

Supported file formats for export:

| File type | Export method |
| :---- | :---- |
| CSV | Dataset.to\_csv() |
| JSON | Dataset.to\_json() |
| Parquet | Dataset.to\_parquet() |
| SQL | Dataset.to\_sql() |
| Pandas | Dataset.to\_pandas() |

**Sources**  
1\. [https://huggingface.co/docs/datasets/process](https://huggingface.co/docs/datasets/process)  
2\. [https://github.com/huggingface/datasets](https://github.com/huggingface/datasets)  
3\. [https://huggingface.co/docs/datasets/process](https://huggingface.co/docs/datasets/process)  
4\. [https://github.com/huggingface/datasets](https://github.com/huggingface/datasets)  
5\. [https://github.com/huggingface/datasets](https://github.com/huggingface/datasets)