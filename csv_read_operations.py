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
    
#__________________________________________________________________________
###########################################################################
# Function to 
def insert_translations_into_translation_dict(source_file_path, target_file_path, translation_dict_file_path):
    # Read in translation dictionary from file
    translation_dict = read_json_dictionary(translation_dict_file_path)
    # Create a temporary two-dimensional array to map from source plain text to target translated text
    temp_mapping = [[],[]]
    # Store source plain texts
    temp_mapping[0] = read_csv_no_changes(source_file_path)
    # Store target translated texts
    temp_mapping[1] = read_csv_with_replacements(target_file_path)

    # Check if the number of rows in each file is the same
    if len(temp_mapping[0]) != len(temp_mapping[1]):
        print("Error: The counts of rows in the input files are not equal.\n")
        return None
    
    # Insert translations into translation dictionary
    previous_key = "supercalifragilisticexpialidocious"
    previous_cons_run_key = None
    # Loop through the temp mapping from top to bottom
    for i in range(len(temp_mapping[0])):
        # After finding a full paragraph to be translated
            if (temp_mapping[0][i] in translation_dict # this key is in the dictionary
                and temp_mapping[0][i] != previous_cons_run_key # this key is not a consolidated run's key
                and previous_key not in translation_dict): # this key has not already been entered
                # This is a full paragraph translation
                # Insert its translation
                translation_dict[temp_mapping[0][i]]['full_paragraph_translated_text'] = temp_mapping[1][i]
                previous_key = temp_mapping[0][i]
            elif(temp_mapping[0][i] in translation_dict[previous_key]['consolidated_runs']):
                # This is a consolidated run
                # Insert its translation
                translation_dict[previous_key]['consolidated_runs'][temp_mapping[0][i]] = temp_mapping[1][i]
                previous_cons_run_key = temp_mapping[0][i] 
            

    return translation_dict

