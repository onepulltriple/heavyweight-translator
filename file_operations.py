import os
import shutil
import file_paths as FP

#__________________________________________________________________________
###########################################################################
# Function to clean up user-entered file paths
def clean_up_file_paths(file_path):
    return file_path.replace("\\","/")

#__________________________________________________________________________
###########################################################################
# Function to copy a file losslessly
def copy_file_losslessly(path_to_existing_source_file, path_to_new_copy):
    try:
        # Ensure the destination folder exists
        os.makedirs(os.path.dirname(path_to_new_copy), exist_ok=True)

        # Copy the file losslessly
        shutil.copy2(path_to_existing_source_file, path_to_new_copy)

        print(f"A master/parent document was found at:\n{path_to_existing_source_file}")
        print(f"A copy was created and stored here:\n{path_to_new_copy}\n")

        return path_to_new_copy

    except FileNotFoundError:
        #print(f"The file path '{output_file}' is not valid.\n")
        #return None
        pass
    
#__________________________________________________________________________
###########################################################################
# Function to save text elements to a text file
def save_to_text_file(output_file, text_elements, delimiter = ""):
    try:
        with open(output_file, 'w', encoding='utf-8-sig') as file:
            for text_element in text_elements:
                file.write(f"{text_element}{delimiter}")
                # when delimiter is a new line, there will be an extra line at the end of the file

    except FileNotFoundError:
        print(f"The file path '{output_file}' is not valid.\n")
        return None
    
#__________________________________________________________________________
###########################################################################
# Function to read a single-column text file and return a list of values
def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return [line.removesuffix("\n") for line in file]
            #return [line.strip() for line in file]
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.\n")
        return None

#__________________________________________________________________________
###########################################################################
# Function to make a directory
def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

#__________________________________________________________________________
###########################################################################
# Function to check if a file was contains today's date
def file_created_today(filename):
    from datetime import datetime
    import re
    import os
    
    for filename in os.listdir(FP.file_path_dictionary["results_history_folder_path"]):
        # Ignore files that are not .docx
        if not filename.lower().endswith(".docx"):
            continue

        # Get today's date
        todays_date = datetime.today().strftime('%Y.%m.%d')

        # Regex to extract the date(s) from the filename
        date_pattern = re.compile(r"(\d{4}\.\d{2}\.\d{2})")
        date_in_filename = date_pattern.search(filename)

        if date_in_filename: # i.e. not None
            file_date = date_in_filename.group(1)
            if file_date == todays_date:
                return True

    return False