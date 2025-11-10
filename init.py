import input_parameters as IP
import file_operations as FO
import file_paths as FP 

#__________________________________________________________________________
###########################################################################
def parent_file_path_dictionary():
    # Create copy of parent source document in target folder
    # Do this step for the parent document only (handles master .docx paths in case subdocuments are in play)
    parent_source_document_path_before_copying  = FO.clean_up_file_paths(IP.path_to_source_parent_document)
    path_to_source_document = FO.copy_file_losslessly(parent_source_document_path_before_copying, FP.path_for_copy_of_source_parent_document)

    return FP.handle_source_file_paths(path_to_source_document, IP.path_to_output_parent_folder)
