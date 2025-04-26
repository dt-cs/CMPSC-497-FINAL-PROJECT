from datasets import Dataset
from datasets import load_dataset
import json
import os
import random

#define the directory containing the book
cur_dir = os.path.dirname(os.path.realpath(__file__))               
json_path = os.path.join(cur_dir,"open_ai_chat_format.jsonl")  

# Load data from JSONL file - read line by line
data_list = []
with open(json_path, 'r') as file:
    for line in file:
        data_list.append(json.loads(line))

# Shuffle the data
random.shuffle(data_list)
     
# Create dataset
dataset = Dataset.from_list(data_list)


#push the dataset to the hub
dataset.push_to_hub("rhinoscript_ft_data_02", private=True)