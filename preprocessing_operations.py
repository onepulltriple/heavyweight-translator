import re
import input_parameters as IP
import dict_operations as DO
 

#__________________________________________________________________________
###########################################################################
# Function to replace problematic elements of a large string
# This function cleans up many of the artifacts created by the online translator
def regex_replacements(original_content):

    preprocessed_content = re.sub(r'[‘’]', r'"', original_content)
    preprocessed_content = re.sub(r"<run (\w*) ?=[\"‘'’“»](\d*)[\"‘'’”«] ?(/?) ?>", r'<run \1="\2"\3>', preprocessed_content)
    preprocessed_content = re.sub(r"<(\w*)/ >", r'<\1/>', preprocessed_content)
    preprocessed_content = re.sub(r"& lt;", r'&lt;', preprocessed_content) # to fix broken less than placeholders
    preprocessed_content = re.sub(r"& gt;", r'&gt;', preprocessed_content) # to fix broken greater than placeholders
    preprocessed_content = re.sub(r"< ?/ ?run ?>", r'</run>', preprocessed_content) # to fix broken closing run tags
    preprocessed_content = re.sub(r"</run ?\n", r'</run>\n', preprocessed_content) # to restore dropped closing brackets 
    preprocessed_content = re.sub(r"&lt;br&gt;", r'&lt;br/&gt;', preprocessed_content) # to close break tags
    preprocessed_content = re.sub(r"<br>", r'&lt;br/&gt;', preprocessed_content) # to close break tags
    
    return preprocessed_content

#__________________________________________________________________________
###########################################################################
# Function to replace common problematic translations on a per-document basis
def document_specific_replacements(preprocessed_content):
    from file_paths import file_path_dictionary

    # Load preprocessing dictionary
    preprocessing_dict = DO.read_json_dictionary(file_path_dictionary["preprocessing_dict_file_path"])
    
    # If a preprocessing dictionary was found
    if(preprocessing_dict):
        # Loop over each key-value pair for the target lang_cult and use regex to make the substitutions
        try:
            for pattern, repl in preprocessing_dict[IP.target_lang_cult].items():
                preprocessed_content = re.sub(pattern, repl, preprocessed_content)
        except KeyError as e:
            print(f"The {IP.target_lang_cult} target language-culture was not found in the preprocessing dictionary.")
    # Otherwise, 
    else:
        pass

    return preprocessed_content