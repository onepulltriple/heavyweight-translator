# Function definitions for dictionary-related tasks
import csv
import pprint
import json
from csv_read_operations import *


#__________________________________________________________________________
###########################################################################
# Function to read in the first two entries of each row of a csv file and store them as key-value pairs in a dictionary
def read_csv_to_dict(file_path):

    data_dict  = {}

    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            # Assuming the first two columns are key and value
            key = row[0]
            value = row[1] if len(row) > 1 else None

            # Store in the dictionary
            data_dict [key] = value

    #pprint.pprint(data_dict) # pretty-prints dictionary to console (alphabetised)
    return data_dict     


#__________________________________________________________________________
###########################################################################
# Function to add the acquired target translations to the translation dictionary
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
    parent_key = ""
    # Loop through the temp mapping from top to bottom
    for i in range(len(temp_mapping[0])):
        current_key = temp_mapping[0][i]
        current_value = temp_mapping[1][i]
        # After finding a full paragraph to be translated
        if (current_key in translation_dict # this key is in the "outer" dictionary
            and current_key not in parent_key # and this key is not part of the parent key
            ): 
            # This is a full paragraph translation
            translation_dict[current_key]['full_paragraph_translated_text'] = current_value
            parent_key = current_key
        elif(temp_mapping[0][i] in translation_dict[parent_key]['consolidated_runs']):
            # This is a consolidated run translation
            translation_dict[parent_key]['consolidated_runs'][current_key]['cons_run_translated_text'] = current_value

    return translation_dict


#__________________________________________________________________________
###########################################################################
# Function to pretty-print a dictionary to a json file
def print_dict_to_json(dict, file_path):
    with open(file_path, "w", encoding='utf-8-sig') as json_file:
        json.dump(dict, json_file, ensure_ascii=False, indent=4)


#__________________________________________________________________________
###########################################################################
# Function to read in a maintained dictionary
def read_json_dictionary(json_dictionary_file_path):
    try:
        with open(json_dictionary_file_path, 'r', encoding='utf-8-sig') as json_dictionary:
            maintained_dictionary = json.load(json_dictionary)
            print(f"A dictionary at '{json_dictionary_file_path}' was found and will be used.\n")

        return maintained_dictionary
    
    except FileNotFoundError:
        print(f"No dictionary found at '{json_dictionary_file_path}'.\n")
        return None
    
    except json.JSONDecodeError:
        print(f"Error decoding JSON file '{json_dictionary_file_path}'.\n")
        return None


#__________________________________________________________________________
###########################################################################
# Function to assemble a dictionary by zipping together two lists
def zip_to_lists_to_dict(csv_data_01, csv_data_02):
    new_dict = {}

    # Check if the number of rows in each file is the same
    if len(csv_data_01) != len(csv_data_02):
        print("Error: The counts of rows in the input files are not equal.\n")
        return None
    else:
        # Iterate over both files simultaneously
        for row_01, row_02 in zip(csv_data_01, csv_data_02, strict=True):
            if row_01 not in new_dict:
                key = row_01
                value = row_02

                # Store each entry in the dictionary
                new_dict[key] = value

        return new_dict