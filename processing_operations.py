if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import constants
    import logging_operations as LO
    import input_parameters as IP
    import dict_operations as DO
    import sys
    import time
    from dict_operations import *
    from extract_and_swap import *
    import os

#__________________________________________________________________________
###########################################################################
def process_document(step, file_path_dictionary):

    #######################################################################
    if 'START LOGGING':
        # Create file to log output
        logfile = open(file_path_dictionary[f"console_log_{step}_file_path"],'w')

        # Start timing
        start_time = time.time()

        # Replace stdout and stderr with a Tee object
        sys.stdout = LO.Tee(sys.stdout, logfile)
        sys.stderr = LO.Tee(sys.stderr, logfile)


    #######################################################################
    # EXECUTE
    # Load maintained dictionary, if there is one
    DO.maint_translation_dict = DO.read_json_dictionary(file_path_dictionary["MAINT_translation_dict_file_path"])
    if DO.maint_translation_dict == None: 
        DO.maint_translation_dict = {}

    print(f"Beginning {step} operations...")

    if step == constants.EXTRACT:
        # Extract the text elements from the source docx file
        extract_or_swap_text_in_docx(file_path_dictionary, step)

        # # Print confirmation message to the console
        # print(f"The text file containing the untranslated source text has been written to: \n{file_path_dictionary["source_language_plain_texts_file_path"]}\n")
        # print(f"An empty text file awaiting translated text in the target language has been written to: \n{file_path_dictionary["target_language_translations_file_path"]}\n")

        # # Create an empty text files to later store retrieved translations
        # save_to_text_file(file_path_dictionary["target_language_translations_file_path"], [], "\n")

    if step == constants.SWAP:
        # Check if the extraction step has been performed
        if (not os.path.isfile(file_path_dictionary["source_language_plain_texts_file_path"])
            and len(read_json_dictionary(file_path_dictionary["TEMP_translation_dict_file_path"])) > 0):
            print(f"No file found at {file_path_dictionary["source_language_plain_texts_file_path"]}")
            print(f"The date in the above file path should be: {IP.operation_date}\n")
            print(f"If the above dates don't match, the operation_date can be set manually in the input parameters. This issue arises when the {constants.EXTRACT} step was performed on a previous date.")
            print(f"Otherwise, it looks like the {constants.EXTRACT} step hasn't been completed yet. Perform the {constants.EXTRACT} step first.\n")
            quit()

        if len(read_json_dictionary(file_path_dictionary["TEMP_translation_dict_file_path"])) > 0:
            # Update the temp translation dictionary to include the retrieved translations
            temp_translation_dict = insert_translations_into_translation_dict(file_path_dictionary["source_language_plain_texts_file_path"], file_path_dictionary["target_language_translations_file_path"], file_path_dictionary["preprocessed_translations_file_path"], file_path_dictionary["TEMP_translation_dict_file_path"])
            # Save updated temp translation dictionary file for later review
            write_dict_to_json(temp_translation_dict, file_path_dictionary["TEMP_translation_dict_file_path"])

            # Merge the temp dictionary into the MAINTAINED dicationary
            extend_json_dictionary(DO.maint_translation_dict, temp_translation_dict)
            # Save updated MAINTAINED translation dictionary file 
            write_dict_to_json(DO.maint_translation_dict, file_path_dictionary["MAINT_translation_dict_file_path"])
            # Save a copy in the results history for later review and comparison via clipboard diff (for users)
            write_dict_to_json(DO.maint_translation_dict, file_path_dictionary["MAINT_translation_dict_file_path_SNAPSHOT"])

            # Swap the translations into the text elements of the source docx file
            extract_or_swap_text_in_docx(file_path_dictionary, step, DO.maint_translation_dict)


    #######################################################################
    if 'STOP LOGGING':
        # Stop timing
        elapsed_time = time.time() - start_time

        # Convert runtime to hours, minutes, seconds, milliseconds
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

        #print(f"Done with '{file_path_dictionary["source_document_file_name_with_extension"]}'.")
        print(f"Total runtime: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} (hh:mm:ss.mmm)")
        #print("__________________________________________________________________________\n\n")

        # Restore real stdout/stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Close log file
        logfile.close()

        # Suppress unusual error message
        #sys.unraisablehook = None