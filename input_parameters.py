from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Variables
source_document_file_name_without_extension = "Test01"

creation_date = datetime.today().strftime('%Y.%m.%d')
#creation_date = "2025.01.01"

source_lang = "de"
source_culture = "DE"
source_lang_cult = source_lang + "-" + source_culture

target_lang = "en"
target_culture = "UK"
target_lang_cult = target_lang + "-" + target_culture
