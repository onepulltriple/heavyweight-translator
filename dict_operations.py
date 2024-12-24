# Function definitions for dictionary-related tasks
import csv
import pprint
import json


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
# Function to read in the entries of each row of a csv file and store them in a dictionary
def read_csv_and_save_to_translation_dict(file_path, target_lang_cult, translation_dict_file_path):

    translation_dict = {
        target_lang_cult : {}
    }

    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ";")
        
        for row in csv_reader:
            term_guid = row[0]
            term_code = row[1]
            standard_translated_text = row[2] if row[2] != "NULL" else None
            custom_translated_text = row[3] if row[3] != "NULL" else None
            term_insertdatetime = row[4] if row[4] != "NULL" else None
            term_updatedatetime = row[5] if row[5] != "NULL" else None

            translation_dict[target_lang_cult][term_code] = {
                   'StandardTranslation' : standard_translated_text,
                     'CustomTranslation' : custom_translated_text,
                     'LegacyTranslation' : None,
                      'DeeplTranslation' : None,
                              'TermGUID' : term_guid,
                    'TermInsertDateTime' : term_insertdatetime,
                    'TermUpdateDateTime' : term_updatedatetime
            }

    print_dict_to_json(translation_dict, translation_dict_file_path)

    #pprint.pprint(translation_dict) # pretty-prints dictionary to console (alphabetised)
    #print(f"A new dictionary was created at '{translation_dict_file_path}' and will be used.\n")    
    return translation_dict    


#__________________________________________________________________________
###########################################################################
# Function to pretty-print a dictionary to a json file
# what to write, where to write it
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