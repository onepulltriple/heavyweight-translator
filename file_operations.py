# Function definitions for SQL query generation

# Function to save text elements to a text file
def save_to_text_file(output_file, 
                      text_elements):
    try:
        with open(output_file, 'w', encoding='utf-8-sig') as file:
            for text_element in text_elements:
                file.write(f"{text_element}\n")

    except FileNotFoundError:
        print(f"The file path '{output_file}' is not valid.\n")
        return None
   
# Function to read a single-column text file and return a list of values
def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return [line.removesuffix("\n") for line in file]
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.\n")
        return None

    

