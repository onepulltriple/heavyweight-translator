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
        # Start counting now that there will be more than just a single document
        file_count = 1
        with os.scandir(FP.cleaned_up_path_to_source_child_folder) as entries:
            for entry in entries:
                if entry.is_file() and IP.keyword_in_child_document_titles in entry.name:
                    file_count +=1
        
        current_file = 2
        for filename in os.listdir(FP.cleaned_up_path_to_source_child_folder):
            # Narrow down treatment to only certain files
            if IP.keyword_in_child_document_titles in filename:
                print("__________________________________________________________________________\n\n")
                print(f"Starting document {current_file} of {file_count}...")
                file_path = FP.cleaned_up_path_to_source_child_folder + "/" + filename
                if os.path.isfile(file_path):
                    # For child documents (subdocuments) the output document paths do not include the target language
                    FP.file_path_dictionary = FP.handle_source_file_paths(file_path, FP.output_folder_for_child_documents, True)
                    processing_operations.process_document(IP.step,FP.file_path_dictionary)
            
                current_file +=1
                print(f"...done with '{FP.file_path_dictionary["source_document_file_name_with_extension"]}'.")

    print("\n")    