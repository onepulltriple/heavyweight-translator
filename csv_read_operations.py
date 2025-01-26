# Function definitions for csv-reading tasks
import csv
import os.path
import sys
from dict_operations import *

#csv.field_size_limit(100000000)
#csv.field_size_limit(sys.maxsize)
import ctypes
MAX_SIGNED_LONG = (1 << (8 * ctypes.sizeof(ctypes.c_long) - 1)) - 1; 
csv.field_size_limit(MAX_SIGNED_LONG)
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
                if len(row) > 0:
                    
                    row[0] = row[0].replace('‘','"')
                    row[0] = row[0].replace('’','"')

                    temp = row[0]
                else:
                    temp = ""
                
                # Append to the array
                csv_data.append(temp) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
