from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Variables
#source_document_file_name_without_extension = "Basic_GenericSendEmailWF_Benutzerhandbuch"
#source_document_file_name_without_extension = "translogica Benutzerhandbuch New Design"
source_document_file_name_without_extension = "translogica Handbuch für Administratoren"
#source_document_file_name_without_extension = "Test01"

creation_date = datetime.today().strftime('%Y.%m.%d')
creation_date = "2025.03.08"

percentage_increment_to_report = 1 #percent

source_lang = "de"
source_culture = "DE"
source_lang_cult = source_lang + "-" + source_culture

#target_lang = "en"
#target_culture = "UK"

target_lang = "it"
target_culture = "IT"
target_lang_cult = target_lang + "-" + target_culture
