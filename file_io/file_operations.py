import os
import shutil
from file_io import file_paths as FP


def clean_up_file_paths(file_path):
    return file_path.replace("\\","/")


def copy_file_losslessly(path_to_existing_source_file, path_to_new_copy):
    try:
        os.makedirs(os.path.dirname(path_to_new_copy), exist_ok=True)

        shutil.copy2(path_to_existing_source_file, path_to_new_copy)

        print(f"A master/parent document was found at:\n{path_to_existing_source_file}")
        print(f"A copy was created and stored here:\n{path_to_new_copy}\n")

        return path_to_new_copy

    except FileNotFoundError:
        pass
    

def save_to_text_file(output_file, text_elements, delimiter = ""):
    try:
        with open(output_file, 'w', encoding='utf-8-sig') as file:
            for text_element in text_elements:
                file.write(f"{text_element}{delimiter}")

    except FileNotFoundError:
        print(f"The file path '{output_file}' is not valid.\n")
        return None
    

def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return [line.removesuffix("\n") for line in file]
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.\n")
        return None


def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def file_created_today(filename):
    from datetime import datetime
    import re
    import os
    
    for filename in os.listdir(FP.file_path_dictionary["results_history_folder_path"]):
        if not filename.lower().endswith(".docx"):
            continue

        todays_date = datetime.today().strftime('%Y.%m.%d')

        date_pattern = re.compile(r"(\d{4}\.\d{2}\.\d{2})")
        date_in_filename = date_pattern.search(filename)

        if date_in_filename:
            file_date = date_in_filename.group(1)
            if file_date == todays_date:
                return True

    return False