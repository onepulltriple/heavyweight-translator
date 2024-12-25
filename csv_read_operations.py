# Function definitions for csv-reading tasks
import csv
import os.path
from dict_operations import *

#__________________________________________________________________________
###########################################################################
# Function to read in a single-column csv file without making changes
# Except that the newline placeholder <*> will be replaced with \n
def read_csv_no_changes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')

            csv_data = []
            for row in csv_reader:
                csv_data.append(row[0]) # .replace('<*>','\n')  DON'T DO THIS YET (not until swapping in)

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
    
#__________________________________________________________________________
###########################################################################
# Function to read in a single-column csv file
# Perform teh following corrections:
# - Converts forward ticks and backs ticks to double quotes
def read_csv_with_replacements(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')

            csv_data = []

            for row in csv_reader:
                row[0] = row[0].replace('‘','“')
                row[0] = row[0].replace('’','”')

                # Append to the array
                csv_data.append(row[0]) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
