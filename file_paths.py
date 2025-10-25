import input_parameters as IP # type: ignore
import constants

#__________________________________________________________________________
###########################################################################
# FOLDER PATHS
document_components_folder_path         = "./private/" + IP.source_document_file_name_without_extension
console_logs_folder_path                = document_components_folder_path + "/" + "00__console_logs"
source_languages_folder_path            = document_components_folder_path + "/" + "01__extractions_in_source_langs"
target_languages_folder_path            = document_components_folder_path + "/" + "02__translations_in_target_langs"
pre_swapping_parts_folder_path          = document_components_folder_path + "/" + "03__pre-swapping_parts"
maintainable_parts_folder_path          = document_components_folder_path + "/" + "04__maintainable_parts"

###########################################################################
# FILE PATHS
source_document_path                   = "./private/" + IP.source_document_file_name_without_extension + ".docx"
output_document_path                   = "./private/" + IP.source_document_file_name_without_extension + "__" + IP.operation_date + "_" + IP.target_lang_cult + ".docx"

dynamic_file_path_names = {
    "console_log_extraction_file_path":  console_logs_folder_path + "/" + IP.operation_datetime + "__" + constants.EXTRACT + "_step_for_" + IP.target_lang_cult + ".log",
    "console_log_swapping_file_path":    console_logs_folder_path + "/" + IP.operation_datetime + "__" + constants.SWAP    + "_step_for_" + IP.target_lang_cult + ".log"
}

source_language_plain_texts_file_path  = source_languages_folder_path    + "/" + IP.operation_date + "__extracted_source_text_elements__" + IP.source_lang_cult + ".csv"
target_language_translations_file_path = target_languages_folder_path    + "/" + IP.operation_date + "__translated_text_elements__"       + IP.target_lang_cult + ".csv"
TEMP_translation_dict_file_path        = pre_swapping_parts_folder_path  + "/" + IP.operation_date + "__TEMP_translation_dict__"          + IP.target_lang_cult + ".json"
preprocessed_translations_file_path    = pre_swapping_parts_folder_path  + "/" + IP.operation_date + "__preprocessed_text_elements__"     + IP.target_lang_cult + ".csv"

preprocessing_dict_file_path           = maintainable_parts_folder_path  + "/" + "PREPROCESSING_dict.json"
FULL_translation_dict_file_path        = maintainable_parts_folder_path  + "/" + "MAINTAINED_translation_dict.json"

# Set up file path to dump unparseable xml strings
start_of_xml_debug_file_path = console_logs_folder_path + "/" + IP.operation_datetime + "__unparseables/"
end_of_xml_debug_file_path = "__xml_debug_" + IP.target_lang_cult + ".xml"
