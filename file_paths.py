import input_parameters as IP # type: ignore
import file_operations as FO
import constants
import os

#__________________________________________________________________________
###########################################################################
# FOLDER PATHS (file paths at bottom)
if 'PREPARE PARENT DOCUMENT AND DIRECTORY':
    # Clean up path to output folder where the output parent document will be stored 
    cleaned_up_path_to_output_parent_folder     = FO.clean_up_file_paths(IP.path_to_output_parent_folder)
    # Derive the name of the subfolder which will be created in the output folder
    # This folder is named after the source parent document
    source_document_file_name_no_extension      = os.path.splitext(os.path.basename(IP.path_to_source_parent_document))[0]
    # Create the path to the copy of the actual source parent document, i.e. the destination of the copy
    path_for_copy_of_source_parent_document     = cleaned_up_path_to_output_parent_folder + "/" + source_document_file_name_no_extension + "__" + IP.source_lang_cult + ".docx"

if 'PREPARE CHILD DOCUMENT DIRECTORY':
    # Clean up path to output folder where the output child documents will be stored 
    #if IP.path_to_source_child_folder != "":
    cleaned_up_path_to_source_child_folder      = FO.clean_up_file_paths(IP.path_to_source_child_folder)
    # Derive the name of the subfolder for child documents, which will be created in the output folder
    # This folder is named after the source child document folder
    output_folder_for_child_documents           = cleaned_up_path_to_output_parent_folder + "/" + os.path.basename(os.path.normpath(cleaned_up_path_to_source_child_folder))

#__________________________________________________________________________
###########################################################################
# Function to dynamically handle file paths
def handle_source_file_paths(path_to_source_document, path_to_output_folder, child=False, file_path_dictionary = {}):

    # Clean up user-entered file path
    any_source_document_path                                            = FO.clean_up_file_paths(path_to_source_document)
    file_path_dictionary["file_path_to_source_document"]                = any_source_document_path

    # Create a folder based on the document's name
    # Extract directory and file name
    source_document_file_name_no_extension                              = os.path.splitext(os.path.basename(any_source_document_path))[0]
    source_document_file_name_with_extension                            = os.path.basename(any_source_document_path)
    file_path_dictionary["source_document_file_name_with_extension"]    = source_document_file_name_with_extension

    # Build then create the document components folder path
    any_parent_output_folder_path                                       = FO.clean_up_file_paths(path_to_output_folder)
    document_components_folder_path                                     = FO.clean_up_file_paths(os.path.join(any_parent_output_folder_path, source_document_file_name_no_extension.replace(IP.source_lang_cult,IP.target_lang_cult)))
    file_path_dictionary["document_components_folder_path"]             = document_components_folder_path
    os.makedirs(document_components_folder_path, exist_ok=True)

    # Prepare the document components subfolders' paths
    console_logs_folder_path                                            = document_components_folder_path + "/" + "00__console_logs"
    source_languages_folder_path                                        = document_components_folder_path + "/" + "01__extractions_in_source_langs"
    target_languages_folder_path                                        = document_components_folder_path + "/" + "02__translations_in_target_langs"
    pre_swapping_parts_folder_path                                      = document_components_folder_path + "/" + "03__pre-swapping_parts"
    maintainable_parts_folder_path                                      = document_components_folder_path + "/" + "04__maintainable_parts"
    results_history_folder_path                                         = document_components_folder_path + "/" + "05__results_history"

    # Create folders for document components and output (if they don't already exist)
    FO.make_folder(console_logs_folder_path)
    FO.make_folder(source_languages_folder_path)
    FO.make_folder(target_languages_folder_path)
    FO.make_folder(pre_swapping_parts_folder_path)
    FO.make_folder(maintainable_parts_folder_path)
    FO.make_folder(results_history_folder_path)

    # Set further dynamic file path names
    file_path_dictionary["console_log_extraction_file_path"]            = console_logs_folder_path + "/" + IP.operation_datetime + "__" + constants.EXTRACT + "_step_for_" + IP.target_lang_cult + ".log"
    file_path_dictionary["console_log_swapping_file_path"]              = console_logs_folder_path + "/" + IP.operation_datetime + "__" + constants.SWAP    + "_step_for_" + IP.target_lang_cult + ".log"

    file_path_dictionary["source_language_plain_texts_file_path"]       = source_languages_folder_path    + "/" + IP.operation_date + "__extracted_source_text_elements__" + IP.source_lang_cult + ".csv"
    file_path_dictionary["target_language_translations_file_path"]      = target_languages_folder_path    + "/" + IP.operation_date + "__translated_text_elements__"       + IP.target_lang_cult + ".csv"
    file_path_dictionary["TEMP_translation_dict_file_path"]             = pre_swapping_parts_folder_path  + "/" + IP.operation_date + "__TEMP_translation_dict__"          + IP.target_lang_cult + ".json"
    file_path_dictionary["preprocessed_translations_file_path"]         = pre_swapping_parts_folder_path  + "/" + IP.operation_date + "__preprocessed_text_elements__"     + IP.target_lang_cult + ".csv"

    file_path_dictionary["preprocessing_dict_file_path"]                = maintainable_parts_folder_path  + "/" + "PREPROCESSING_dict.json"
    file_path_dictionary["FULL_translation_dict_file_path"]             = maintainable_parts_folder_path  + "/" + "MAINTAINED_translation_dict.json"

    # Set the file path to dump unparseable xml strings
    file_path_dictionary["start_of_xml_debug_file_path"]                = console_logs_folder_path + "/" + IP.operation_datetime + "__unparseables/"
    file_path_dictionary["end_of_xml_debug_file_path"]                  = "__xml_debug_" + IP.target_lang_cult + ".xml"

    # Set the output document paths
    file_path_dictionary["output_document_path_with_datetime"]          = results_history_folder_path + "/" + source_document_file_name_no_extension.replace(IP.source_lang_cult,IP.target_lang_cult) + "__" + IP.operation_datetime + ".docx"
    if child == False:
        file_path_dictionary["output_document_path"]                    = any_parent_output_folder_path + "/" + source_document_file_name_no_extension.replace(IP.source_lang_cult,IP.target_lang_cult) + ".docx"
    else:
        file_path_dictionary["output_document_path"]                    = any_parent_output_folder_path + "/" + source_document_file_name_no_extension + ".docx"

    return file_path_dictionary


#__________________________________________________________________________
###########################################################################
# Function to handle the parent/master (or only) document
def parent_file_path_dictionary():
    # Create copy of parent source document in target folder
    # Do this step for the parent document only (handles master .docx paths in case subdocuments are in play)
    parent_source_document_path_before_copying  = FO.clean_up_file_paths(IP.path_to_source_parent_document)
    path_to_source_document = FO.copy_file_losslessly(parent_source_document_path_before_copying, path_for_copy_of_source_parent_document)

    return handle_source_file_paths(path_to_source_document, IP.path_to_output_parent_folder)


#__________________________________________________________________________
###########################################################################
# FILE PATHS
# Initialize file path dictionary
file_path_dictionary = None