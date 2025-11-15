from datetime import datetime
import constants

#__________________________________________________________________________
###########################################################################
# SET MODE OF EXECUTION
# Select one by commenting the other(s) out
step = constants.EXTRACT
step = constants.SWAP

#__________________________________________________________________________
###########################################################################
# SET PATHS TO FILES/FOLDERS
# Enter a full or relative file path preceded by 'r' and wrapped in double quotes, for example:
# path_to_source_parent_document        = r"N:\example_output_folder_name\subfolder_name\Admin_Datenbankstruktur.docx"
# path_to_output_parent_folder          = r"N:\example_output_folder_name\subfolder_name"
# In Microsoft Windows, Shift + Right-click on source document, then select 'Copy as path'
path_to_source_parent_document          = r"N:\test_zentralen\test_Handbuch für Administratoren.docx"
#path_to_output_child_folder             = r"N:\new english central\filialen"
path_to_output_parent_folder            = r"N:\new english central"


#__________________________________________________________________________
###########################################################################
# SET LANGUAGE PARAMETERS
# Set the language of the source document
source_language                         = "de"
source_culture                          = "DE"
source_lang_cult                        = source_language + "-" + source_culture

# Set the language of the target document
target_language                         = "en"
target_culture                          = "GB"
target_lang_cult                        = target_language + "-" + target_culture


#__________________________________________________________________________
###########################################################################
# SET REPORTING PARAMETERS
# Set the progress reporting frequency (prints progress to console after every % increment completed)
percentage_increment_to_report          = 1 


#__________________________________________________________________________
###########################################################################
# SET OPERATION DATE/TIME
# Operation date and time (comment in last line to set manually)
operation_datetime                      = datetime.today().strftime('%Y.%m.%d %H.%M') # https://docs.python.org/3/library/time.html#time.strftime
operation_date                          = datetime.today().strftime('%Y.%m.%d')
#operation_date                          = "2025.10.19" # yyyy.MM.dd