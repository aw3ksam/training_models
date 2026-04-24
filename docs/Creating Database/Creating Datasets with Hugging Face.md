# **Create a dataset**

Sometimes, you may need to create a dataset if you're working with your own data. Creating a dataset with 🤗 Datasets confers all the advantages of the library: fast loading and processing, streaming enormous datasets, memory-mapping, and more.  
This tutorial covers low-code methods for creating datasets:

* **File-based builders** for common formats (CSV, JSON, Parquet).  
* **Folder-based builders** for image and audio data.  
* **From Python dictionaries** and generators.

## ---

**File-based builders**

🤗 Datasets supports many common formats such as csv, json/jsonl, parquet, and txt.

Python

from datasets import load\_dataset  
dataset \= load\_dataset("csv", data\_files="my\_file.csv")

## ---

**Folder-based builders**

ImageFolder and AudioFolder are low-code methods for quickly creating datasets from local directories. They automatically generate features, splits, and labels based on the directory structure.

### **ImageFolder**

Label names are inferred from directory names. For a structure like pokemon/train/grass/bulbasaur.png, the label will be grass.

Python

from datasets import load\_dataset  
dataset \= load\_dataset("imagefolder", data\_dir="/path/to/pokemon")

### **AudioFolder**

Works identically to ImageFolder, but for audio files (supporting wav, mp3, mp4, etc.).

Python

from datasets import load\_dataset  
dataset \= load\_dataset("audiofolder", data\_dir="/path/to/folder")

### **Metadata**

Additional information (captions, transcriptions) can be included via a metadata.csv file in the folder. It must contain a file\_name column.

Code snippet

file\_name, text  
bulbasaur.png, There is a plant seed on its back...  
charmander.png, It has a preference for hot things.

## ---

**From Python dictionaries**

### **from\_generator()**

The most memory-efficient way to create a dataset. It generates the dataset on disk progressively and memory-maps it.

Python

from datasets import Dataset

def gen():  
    yield {"pokemon": "bulbasaur", "type": "grass"}  
    yield {"pokemon": "squirtle", "type": "water"}

ds \= Dataset.from\_generator(gen)

For an **IterableDataset**:

Python

from datasets import IterableDataset  
ds \= IterableDataset.from\_generator(gen)

### **from\_dict()**

A straightforward way to create a dataset from a standard dictionary.

Python

from datasets import Dataset  
ds \= Dataset.from\_dict({"pokemon": \["bulbasaur", "squirtle"\], "type": \["grass", "water"\]})

To create an image or audio dataset this way, use cast\_column():

Python

from datasets import Audio  
audio\_dataset \= Dataset.from\_dict({"audio": \["path/to/audio\_1"\]}).cast\_column("audio", Audio())  
