from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Variables
#source_document_file_name_without_extension = "Basic_GenericSendEmailWF_Benutzerhandbuch"
#source_document_file_name_without_extension = "translogica Benutzerhandbuch New Design"
#source_document_file_name_without_extension = "19.09.2025__translogica Benutzerhandbuch"
source_document_file_name_without_extension = "BeispielTDB"

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
