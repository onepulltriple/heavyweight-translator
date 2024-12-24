if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import sys
    import os
    import constants 
    import input_parameters as IP 
    import file_paths as FP 
    from collections import OrderedDict
    from dict_operations import *
    from text_operations import *
    from file_operations import *
    from extract_and_swap import *
    print("\n")

#__________________________________________________________________________
###########################################################################
if 'SET MODE OF EXECUTION':
    # Select one by commenting the others out
    step = constants.EXTRACT

#__________________________________________________________________________
###########################################################################
# EXECUTE
if step == constants.EXTRACT:
    # Extract the text elements from the source docx file
    print(f"Beginning {step} operations...")
    extract_or_swap_text_in_docx(FP.source_document_path, step)

    # Deduplicate the extracted text elements and store them in a list
    #list_of_deduplicated_source_text_elements = list(OrderedDict.fromkeys(original_txt_data))

    # Dump deduplicated list into a text file so it can be translated
    # save_to_text_file(FP.source_language_deduplicated_file_path, 
    #                   list_of_deduplicated_source_text_elements)

    # Print confirmation message to the console
    print(f"The text file containing the untranslated source text has been written to: \n{FP.source_language_plain_texts_file_path}\n")

    # Create the remaining empty text files
    save_to_text_file(FP.target_language_translations_file_path, [])
    if not os.path.exists(FP.poor_deepl_translations_file_path):
        save_to_text_file(FP.poor_deepl_translations_file_path, [])
    if not os.path.exists(FP.corrected_deepl_translations_file_path):
        save_to_text_file(FP.corrected_deepl_translations_file_path, [])