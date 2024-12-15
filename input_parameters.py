from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Variables
source_document_file_name_without_extension = "Benutzerhandbuch"

#creation_date = "2024.11.22"
creation_date = datetime.today().strftime('%Y.%m.%d')

source_lang = "de"
source_culture = "DE"
source_lang_cult = source_lang + "-" + source_culture

target_lang = "en"
target_culture = "UK"
target_lang_cult = target_lang + "-" + target_culture
