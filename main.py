if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import file_paths as FP
    import input_parameters as IP
    import processing_operations
    import os
    import time
    print("\n")


#######################################################################
if 'START GLOBAL TIMER':
    # Start timing
    total_start_time = time.time()


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
                file_path = FP.cleaned_up_path_to_source_child_folder + "/" + filename
                if os.path.isfile(file_path):
                    # For child documents (subdocuments) the output document paths do not include the target language
                    FP.file_path_dictionary = FP.handle_source_file_paths(file_path, FP.output_folder_for_child_documents, True)
                    print("__________________________________________________________________________\n\n")
                    print(f"Starting document {current_file} of {file_count}, which is named: '{FP.file_path_dictionary["source_document_file_name_with_extension"]}'")
                    processing_operations.process_document(IP.step,FP.file_path_dictionary)
            
                current_file +=1
                print(f"...done with '{FP.file_path_dictionary["source_document_file_name_with_extension"]}'.")


#######################################################################
if 'STOP GLOBAL TIMER':
    # Stop timing
    total_elapsed_time = time.time() - total_start_time

    # Convert runtime to hours, minutes, seconds, milliseconds
    hours = int(total_elapsed_time // 3600)
    minutes = int((total_elapsed_time % 3600) // 60)
    seconds = int(total_elapsed_time % 60)
    milliseconds = int((total_elapsed_time - int(total_elapsed_time)) * 1000)

    print(f"\nTotal runtime for all processes: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} (hh:mm:ss.mmm)")
    print("\n")    