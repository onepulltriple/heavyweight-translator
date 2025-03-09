# Function definitions for csv-reading tasks
import csv
from dict_operations import *
from preprocessing_operations import *

import ctypes
MAX_SIGNED_LONG = (1 << (8 * ctypes.sizeof(ctypes.c_long) - 1)) - 1; 
csv.field_size_limit(MAX_SIGNED_LONG)
#__________________________________________________________________________
###########################################################################
# Function to read in a single-column csv file without making changes
def read_csv_no_changes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, quotechar='¥', delimiter='¥')

            csv_data = []
            for row in csv_reader:
                csv_data.append(row[0]) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None

#__________________________________________________________________________
###########################################################################
# Function to preprocess a single-column csv file
# Perform the following corrections:
# - Converts forward ticks and backs ticks to double quotes
def preprocess_csv(original_file_path, preprocessed_file_path):
    try:
        # Open original file
        with open(original_file_path, 'r', encoding='utf-8-sig') as csv_file:
            original_content = csv_file.read()

        # Preprocess
        altered_content = regex_replacements(original_content)

        # Save preprocessed file as new file
        with open(preprocessed_file_path, 'w', encoding='utf-8-sig') as csv_file:
            csv_file.write(altered_content)
        
    except FileNotFoundError:
        print(f"No file found at '{original_file_path}'.")
        return None

    
#__________________________________________________________________________
###########################################################################
# Function to read in a single-column csv file
def read_csv_with_replacements(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, quotechar='¥', delimiter='¥', lineterminator='\n')
            csv_data = []

            for row in csv_reader:
                if len(row) > 0:
                    temp = row[0]
                else:
                    temp = ""
                
                # Append to the array
                csv_data.append(temp) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
