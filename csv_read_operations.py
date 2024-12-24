# Function definitions for csv-reading tasks
import csv
import os.path
    
#__________________________________________________________________________
###########################################################################
# Function to read in a single-column csv file without making changes
def read_csv_no_changes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')

            csv_data = []
            for row in csv_reader:
                csv_data.append(row[0])

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
                csv_data.append(row) 

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
    
#__________________________________________________________________________
###########################################################################
# Function to 
def read_translation_dict_from_csv(source_file_path, target_file_path, translation_dict):
    # Create a temporary two-dimensional array to map from source plain text to target translated text
    temp_mapping = [[],[]]
    # Store source plain texts
    temp_mapping[0] = read_csv_no_changes(source_file_path)
    # Store target translated texts
    temp_mapping[1] = read_csv_with_replacements(target_file_path)

    # Insert translations into translation dictionary
    for i in range(len(temp_mapping[0])):
        # Insert full paragraph translations
        source_plain_text = temp_mapping[0][i]
        if source_plain_text in translation_dict:
            translation_dict[source_plain_text]['full_paragraph_translated_text'] = temp_mapping[1][i]

    # Insert array contents into dictionary
    for translation in csv_data:
        pass
    return csv_data

