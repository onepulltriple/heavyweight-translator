if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import file_paths as FP
    import input_parameters as IP
    import processing_operations
    import os
    print("\n")


#__________________________________________________________________________
###########################################################################
if 'PROCESS ONE OR MORE DOCUMENTS':
        
    # For a single, large document or a master document with subdocuments, 
    # there will always be at least one document to process
    if FP.file_path_dictionary is None:
        FP.file_path_dictionary = FP.parent_file_path_dictionary()

    # Process single/parent document
    processing_operations.process_document(IP.step,FP.file_path_dictionary)

    # Process child documents
    if FP.cleaned_up_path_to_source_child_folder != "":
        for filename in os.listdir(FP.cleaned_up_path_to_source_child_folder):
            # Narrow down treatment to only certain files
            if IP.keyword_in_child_document_titles in filename:
                file_path = FP.cleaned_up_path_to_source_child_folder + "/" + filename
                if os.path.isfile(file_path):
                    # For child documents (subdocuments) the output document paths do not include the target language
                    FP.file_path_dictionary = FP.handle_source_file_paths(file_path, FP.output_folder_for_child_documents, True)
                    processing_operations.process_document(IP.step,FP.file_path_dictionary)
