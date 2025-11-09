from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Variables
#source_document_file_name_without_extension = "translogica Benutzerhandbuch New Design"
#source_document_file_name_without_extension = "19.09.2025__translogica Benutzerhandbuch"
#source_document_file_name_without_extension = "BeispielTDB"

#full_path_to_source_document = "N:\\test_zentralen\\filialen\\Admin_Datenbankstruktur.docx"
full_path_to_source_document = "C:\\Users\\Chase Helgenlechner\\Documents\\00__Coding Projects\\01__Translation Projects\\03__heavyweight-translator\\private\\Anwendungsfall.docx"
#full_path_to_output_folder   = "N:\\test_zentralen\\filialen"
full_path_to_output_folder   = "C:\\Users\\Chase Helgenlechner\\Downloads\\__target folder"
relative_path_to_source_document = None

operation_datetime = datetime.today().strftime('%Y.%m.%d %H.%M') # https://docs.python.org/3/library/time.html#time.strftime
operation_date = datetime.today().strftime('%Y.%m.%d')
#operation_date = "2025.10.19" # yyyy.MM.dd


percentage_increment_to_report = 1 #percent

source_language = "de"
source_culture = "DE"
source_lang_cult = source_language + "-" + source_culture

target_language = "en"
target_culture = "GB"
target_lang_cult = target_language + "-" + target_culture
