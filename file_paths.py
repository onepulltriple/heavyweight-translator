import file_operations as FO
import input_parameters as IP # type: ignore
import constants

#__________________________________________________________________________
###########################################################################
# FILE PATHS
document_components_path               = "./private/" + IP.source_document_file_name_without_extension + "__" + IP.operation_date
source_document_path                   = "./private/" + IP.source_document_file_name_without_extension + ".docx"
#output_document_path                   = document_components_path + "/" + IP.source_document_file_name_without_extension + "_" + IP.target_lang_cult + ".docx"
output_document_path                   = "./private/" + IP.source_document_file_name_without_extension + "__" + IP.operation_date + "_" + IP.target_lang_cult + ".docx"


dynamic_file_path_names = {
    "console_log_extraction_file_path":  document_components_path + "/" + "00__console_log_of_" + constants.EXTRACT + "_step_at_" + IP.operation_datetime + "_for_" + IP.target_lang_cult + ".log",
    "console_log_swapping_file_path":    document_components_path + "/" + "06__console_log_of_" + constants.SWAP    + "_step_at_" + IP.operation_datetime + "_for_" + IP.target_lang_cult + ".log"
}


source_language_plain_texts_file_path  = document_components_path + "/" + "01__extracted_source_text_elements_" + IP.source_lang_cult + ".csv"
target_language_translations_file_path = document_components_path + "/" + "02__translated_text_elements_" + IP.target_lang_cult + ".csv"
TEMP_translation_dict_file_path        = document_components_path + "/" + "03__TEMP_translation_dict_" + IP.target_lang_cult + ".json"

document_specific_regex_dict_file_path = document_components_path + "/" + "04__regex_dict_" + IP.target_lang_cult + ".json"
preprocessed_translations_file_path    = document_components_path + "/" + "05__preprocessed_text_elements_" + IP.target_lang_cult + ".csv"
FULL_translation_dict_file_path        = document_components_path + "/" + "07__FULL_translation_dict_" + IP.target_lang_cult + ".json"
#MAINT_translation_dict_file_path        = document_components_path + "/" + "07__maintainted_translation_dict_" + IP.target_lang_cult + ".json"

# Set up file path to dump unparseable xml strings
start_of_xml_debug_file_path = document_components_path + "/unparseables/"
end_of_xml_debug_file_path = "__xml_debug_" + IP.target_lang_cult + ".xml"



# Set up file path for dictionaries
#master_document_file_path = document_components_path + "/master"
#FO.make_folder(master_document_file_path)
#subdocuments_file_path = document_components_path + "/subdocuments"
#FO.make_folder(subdocuments_file_path)
#versions_file_path = document_components_path + "/versions"
#FO.make_folder(versions_file_path)
