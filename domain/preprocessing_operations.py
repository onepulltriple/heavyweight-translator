import re
from app import input_parameters as IP
from file_io import dict_operations as DO


def regex_replacements(original_content):

    preprocessed_content = re.sub(r'[‘’]', r'"', original_content)
    preprocessed_content = re.sub(
        r"<?run (\w*) ?=[\"‘'’“»](\d*)[\"‘'’”«] ?(/?) ?>", 
        r'<run \1="\2"\3>', preprocessed_content
    )
    preprocessed_content = re.sub(r"<(\w*)/ >", r'<\1/>', preprocessed_content)
    preprocessed_content = re.sub(r"& lt;", r'&lt;', preprocessed_content) 
    preprocessed_content = re.sub(r"& gt;", r'&gt;', preprocessed_content) 
    preprocessed_content = re.sub(r"< ?/ ?run ?>", r'</run>', preprocessed_content) 
    preprocessed_content = re.sub(r"</run ?\n", r'</run>\n', preprocessed_content) 
    preprocessed_content = re.sub(r"&lt;br&gt;", r'&lt;br/&gt;', preprocessed_content) 
    preprocessed_content = re.sub(r"<br>", r'&lt;br/&gt;', preprocessed_content) 
    
    return preprocessed_content


def document_specific_replacements(preprocessed_content):
    from file_io.file_paths import file_path_dictionary

    preprocessing_dict = DO.read_json_dictionary(
        file_path_dictionary["preprocessing_dict_file_path"]
    )
    
    if(preprocessing_dict):
        try:
            for pattern, repl in preprocessing_dict[IP.target_lang_cult].items():
                preprocessed_content = re.sub(
                    pattern, repl, preprocessed_content
                )
        except KeyError as e:
            print(
                f"The {IP.target_lang_cult} target language-culture "
                "was not found in the preprocessing dictionary."
            )

    return preprocessed_content