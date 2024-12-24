# Function definitions for text-related tasks
import os.path

#__________________________________________________________________________
###########################################################################
# Function to read a single-column text file and return a list of values
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return [line.strip() for line in file]
