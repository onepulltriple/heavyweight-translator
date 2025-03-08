if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
#    import sys
#    import os
    import constants 
    import file_paths as FP 
    from dict_operations import *
    from file_operations import *
    from extract_and_swap import *
    print("\n")

#__________________________________________________________________________
###########################################################################
if 'SET MODE OF EXECUTION':
    # Select one by commenting the others out
    step = constants.EXTRACT
    step = constants.SWAP

#__________________________________________________________________________
###########################################################################
# EXECUTE
print(f"Beginning {step} operations...")

if step == constants.EXTRACT:
    # Extract the text elements from the source docx file
    extract_or_swap_text_in_docx(FP.source_document_path, step)

    # Print confirmation message to the console
    print(f"The text file containing the untranslated source text has been written to: \n{FP.source_language_plain_texts_file_path}\n")

    # Create an empty text files to later store translations
    #if not os.path.exists(FP.target_language_translations_file_path):
    save_to_text_file(FP.target_language_translations_file_path, [], "\n")

if step == constants.SWAP:
    # Update the translation dictionary to include the retrieved translations
    translation_dict = insert_translations_into_translation_dict(FP.source_language_plain_texts_file_path, FP.target_language_translations_file_path, FP.TEMP_translation_dict_file_path)

    # Save updated translation dictionary file for later review
    write_dict_to_json(translation_dict, FP.FULL_translation_dict_file_path)

    # Swap the text elements from the source docx file
    extract_or_swap_text_in_docx(FP.source_document_path, step, translation_dict, FP.output_document_path)