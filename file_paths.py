import os
import input_parameters as IP # type: ignore

#__________________________________________________________________________
###########################################################################
# FILE PATHS
source_document_path                   = "./private/" + IP.source_document_file_name_without_extension + ".docx"
output_document_path                   = "./private/" + IP.source_document_file_name_without_extension + "_" + IP.target_lang_cult + ".docx"
document_components_path               = "./private/" + IP.creation_date + "__" + IP.source_document_file_name_without_extension
if not os.path.exists(document_components_path):
    os.makedirs(document_components_path)

deepl_dict_file_path                   = document_components_path + "/" + IP.source_lang_cult + "_" + IP.target_lang_cult + "_dict_from_deepl.json"
maintained_dictionary_file_path        = document_components_path + "/" + IP.source_lang_cult + "_" + IP.target_lang_cult + "_dict_maintained.json"
correction_dict_file_path              = document_components_path + "/" + IP.source_lang_cult + "_" + IP.target_lang_cult + "_dict_corrections.json"
composite_dict_file_path               = document_components_path + "/" + IP.source_lang_cult + "_" + IP.target_lang_cult + "_dict_composite.json"
source_language_deduplicated_file_path = document_components_path + "/" + "01__extracted_deduplicated_text_elements_" + IP.source_lang_cult + ".txt"
target_language_translations_file_path = document_components_path + "/" + "02__translated_text_elements_" + IP.target_lang_cult + ".txt"
poor_deepl_translations_file_path      = document_components_path + "/" + "03__poor_deepl_translations_" + IP.target_lang_cult + ".txt"
corrected_deepl_translations_file_path = document_components_path + "/" + "04__corrected_deepl_translations_" + IP.target_lang_cult + ".txt"
TEMP_translation_dict_file_path        = document_components_path + "/" + "05__TEMP_translation_dict_" + IP.target_lang_cult + ".json"
