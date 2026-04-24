# **Know your dataset**

There are two types of dataset objects: a regular **Dataset** and an **IterableDataset**.

* **Dataset**: Provides fast random access to rows and uses memory-mapping to handle large datasets with minimal device memory.  
* **IterableDataset**: Allows access to massive datasets that do not fit on disk or in memory by streaming them.

## ---

**Dataset**

Loading a dataset split typically returns a Dataset object.

Python

from datasets import load\_dataset  
dataset \= load\_dataset("cornell-movie-review-data/rotten\_tomatoes", split="train")

### **Indexing**

Access examples using axis labels or column names.

* **By Row**: Returns a dictionary of the example.  
  Python  
  \# First row  
  \>\>\> dataset\[0\]  
  \# Last row  
  \>\>\> dataset\[-1\]

* **By Column**: Returns a list of all values in that column.  
  Python  
  \>\>\> dataset\["text"\]

* **Combined**:  
  Python  
  \>\>\> dataset\[0\]\["text"\]  
  \>\>\> dataset\["text"\]\[0\]

### **Slicing**

Returns a subset of the dataset as a dictionary of lists.

Python

\# First three rows  
\>\>\> dataset\[:3\]  
\# Rows 3 to 5  
\>\>\> dataset\[3:6\]

## ---

**IterableDataset**

An IterableDataset is loaded by setting streaming=True in load\_dataset().

Python

from datasets import load\_dataset  
iterable\_dataset \= load\_dataset("ethz/food101", split="train", streaming=True)

### **Indexing**

IterableDataset does **not** support random access. You must iterate over elements.

* **Iteration**:  
  Python  
  \# Using next()  
  \>\>\> next(iter(iterable\_dataset))

  \# Using a loop  
  \>\>\> for example in iterable\_dataset:  
  ...     print(example)  
  ...     break

* **Column Indexing**: Returns an iterable for specific column values.  
  Python  
  \>\>\> next(iter(iterable\_dataset\["label"\]))

### **Creating a subset**

Use take() to create a new IterableDataset containing a specific number of examples.

Python

\# Get first three examples  
\>\>\> list(iterable\_dataset.take(3))

## ---

**Next Steps**

* **Differences**: Consult the "Differences between Dataset and IterableDataset" guide.  
* **Processing**: See the **Process** guide for Dataset or the **Stream** guide for IterableDataset.