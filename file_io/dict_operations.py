import csv
import json
from app import input_parameters as IP
from file_io import csv_read_operations as CSVR


def read_csv_to_dict(file_path):
    data_dict = {}

    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            key = row[0]
            value = row[1] if len(row) > 1 else None

            data_dict [key] = value

    return data_dict     


def insert_translations_into_translation_dict(source_file_path, target_file_path, preprocessed_file_path, temp_translation_dict_file_path):
    temp_translation_dict = read_json_dictionary(temp_translation_dict_file_path)
    temp_mapping = [[],[]]
    temp_mapping[0] = CSVR.read_csv_no_changes(source_file_path)
    CSVR.preprocess_csv(target_file_path, preprocessed_file_path)
    temp_mapping[1] = CSVR.read_csv_with_replacements(preprocessed_file_path)

    if len(temp_mapping[0]) != len(temp_mapping[1]):
        print("Error: The counts of rows of the input files are not equal. This check occurs after preprocessing.")
        print("Review the following files:")
        print(f"{source_file_path}")
        print(f"{preprocessed_file_path}\n")
        quit()

    for i in range(0, len(temp_mapping[0])):
        current_key = temp_mapping[0][i]
        current_value = temp_mapping[1][i]
        if current_key in temp_translation_dict: 
            temp_translation_dict[current_key][IP.target_lang_cult] = current_value

    return temp_translation_dict


def write_dict_to_json(dict, file_path):
    with open(file_path, "w", encoding='utf-8-sig') as json_file:
        json.dump(dict, json_file, ensure_ascii=False, indent=4)


def extend_json_dictionary(original_dict, new_portion):
    original_dict |= new_portion
    return original_dict


def read_json_dictionary(json_dictionary_file_path):
    try:
        with open(json_dictionary_file_path, 'r', encoding='utf-8-sig') as json_dictionary:
            json_dictionary = json.load(json_dictionary)

        return json_dictionary
    
    except FileNotFoundError:
        return None
    
    except json.JSONDecodeError:
        print(f"Error decoding JSON file '{json_dictionary_file_path}'.\n")
        return None


maint_translation_dict = {}