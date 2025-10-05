if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import constants 
    import file_paths as FP 
    import logging_operations as LO
    import sys
    from dict_operations import *
    from file_operations import *
    from extract_and_swap import *
    print("\n")

#__________________________________________________________________________
###########################################################################
if 'SET MODE OF EXECUTION':
    # Select one by commenting the other(s) out
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

    # Create an empty text files to later store retrieved translations
    save_to_text_file(FP.target_language_translations_file_path, [], "\n")

if step == constants.SWAP:
    # Create file to log output
    logfile = open(console_log_file_path,'w')

    # Replace stdout and stderr with a Tee object
    sys.stdout = LO.Tee(sys.stdout, logfile)
    sys.stderr = LO.Tee(sys.stderr, logfile)

    # Update the translation dictionary to include the retrieved translations
    translation_dict = insert_translations_into_translation_dict(FP.source_language_plain_texts_file_path, FP.target_language_translations_file_path, FP.preprocessed_translations_file_path, FP.TEMP_translation_dict_file_path)

    # Save updated translation dictionary file for later review
    write_dict_to_json(translation_dict, FP.FULL_translation_dict_file_path)

    # Swap the translations into the text elements of the source docx file
    extract_or_swap_text_in_docx(FP.source_document_path, step, translation_dict, FP.output_document_path)

    # Close log file
    logfile.close()