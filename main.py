if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import init
    #import constants 
    #import file_paths as FP 
    import logging_operations as LO
    import input_parameters as IP
    #import file_operations as FO
    import sys
    import time
    from dict_operations import *
    from extract_and_swap import *
    import os
    import somewhere_else
    print("\n")


#__________________________________________________________________________
###########################################################################
if 'PROCESS ONE OR MORE DOCUMENTS':
        
    # For a single, large document or a master document with subdocuments, 
    # there will always be at least one document to process
    if init.file_path_dictionary is None:
        init.file_path_dictionary = init.parent_file_path_dictionary()

    # Process single/parent document
    somewhere_else.amain(IP.step,init.file_path_dictionary)

    # Loop over documents and send them through main
    # main should probably take the file path dictionary as an argument
    # mode of execution maybe belongs in input parameters 





# #__________________________________________________________________________
# ###########################################################################
# if 'SET MODE OF EXECUTION':
#     # Select one by commenting the other(s) out
#     step = constants.EXTRACT
#     #step = constants.SWAP

# #__________________________________________________________________________
# ###########################################################################
# def amain(step, file_path_dictionary):

#     #######################################################################
#     if 'START LOGGING':
#         # Create file to log output
#         logfile = open(file_path_dictionary[f"console_log_{step}_file_path"],'w')

#         # Start timing
#         start_time = time.time()

#         # Replace stdout and stderr with a Tee object
#         sys.stdout = LO.Tee(sys.stdout, logfile)
#         sys.stderr = LO.Tee(sys.stderr, logfile)


#     #######################################################################
#     # EXECUTE
#     print(f"Beginning {step} operations...")

#     if step == constants.EXTRACT:
#         # Extract the text elements from the source docx file
#         extract_or_swap_text_in_docx(file_path_dictionary, step)

#         # Print confirmation message to the console
#         print(f"The text file containing the untranslated source text has been written to: \n{file_path_dictionary["source_language_plain_texts_file_path"]}\n")

#         # Create an empty text files to later store retrieved translations
#         save_to_text_file(file_path_dictionary["target_language_translations_file_path"], [], "\n")

#     if step == constants.SWAP:
#         # Check if the extraction step has been performed
#         if not os.path.isfile(file_path_dictionary["source_language_plain_texts_file_path"]):
#             print(f"No file found at {file_path_dictionary["source_language_plain_texts_file_path"]}")
#             print(f"The date in the above file path should be: {IP.operation_date}\n")
#             print(f"If the above dates don't match, the operation_date can be set manually in the input parameters. This issue arises when the {constants.EXTRACT} step was performed on a previous date.")
#             print(f"Otherwise, it looks like the {constants.EXTRACT} step hasn't been completed yet. Perform the {constants.EXTRACT} step first.\n")
#             quit()

#         # Update the translation dictionary to include the retrieved translations
#         translation_dict = insert_translations_into_translation_dict(file_path_dictionary["source_language_plain_texts_file_path"], file_path_dictionary["target_language_translations_file_path"], file_path_dictionary["preprocessed_translations_file_path"], file_path_dictionary["TEMP_translation_dict_file_path"])

#         # Save updated translation dictionary file for later review
#         write_dict_to_json(translation_dict, file_path_dictionary["FULL_translation_dict_file_path"])

#         # Swap the translations into the text elements of the source docx file
#         extract_or_swap_text_in_docx(file_path_dictionary, step, translation_dict)


#     #######################################################################
#     if 'STOP LOGGING':
#         # Stop timing
#         elapsed_time = time.time() - start_time

#         # Convert runtime to hours, minutes, seconds, milliseconds
#         hours = int(elapsed_time // 3600)
#         minutes = int((elapsed_time % 3600) // 60)
#         seconds = int(elapsed_time % 60)
#         milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

#         print(f"Total runtime: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} (hh:mm:ss.mmm)\n")

#         # Close log file
#         logfile.close()

#         # Suppress unusual error message
#         sys.unraisablehook = None