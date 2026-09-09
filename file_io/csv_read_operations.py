import csv
import os
from domain import preprocessing_operations as PREPOP

import ctypes
MAX_SIGNED_LONG = (1 << (8 * ctypes.sizeof(ctypes.c_long) - 1)) - 1; 
csv.field_size_limit(MAX_SIGNED_LONG)


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


def preprocess_csv(original_file_path, preprocessed_file_path):
    try:
        with open(original_file_path, 'r', encoding='utf-8-sig') as csv_file:
            original_content = csv_file.read()

        if os.stat(original_file_path).st_size == 0:
            print("Error: Empty input file encountered. This check occurs before preprocessing.")
            print(f"Were translations added to the following file?:")
            print(f"{original_file_path}\n")
            quit()

        altered_content = PREPOP.regex_replacements(original_content)
        altered_content = PREPOP.document_specific_replacements(altered_content)
        print("Preprocessing completed...")

        with open(preprocessed_file_path, 'w', encoding='utf-8-sig') as csv_file:
            csv_file.write(altered_content)
        
    except FileNotFoundError:
        print(f"No file found at '{original_file_path}'.")
        return None

    
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
                
                csv_data.append(temp) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None