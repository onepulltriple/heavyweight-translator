if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import os
    import time
    from app import input_parameters as IP
    from domain import processing_operations as PROC
    from file_io import file_paths as FP
    print("\n")

if 'START GLOBAL TIMER':
    total_start_time = time.time()

if 'PROCESS ONE OR MORE DOCUMENTS':
    if FP.file_path_dictionary is None:
        FP.file_path_dictionary = FP.parent_file_path_dictionary()

    PROC.process_document(IP.step,FP.file_path_dictionary)

    if FP.cleaned_up_path_to_source_child_folder != "":
        file_count = 1
        with os.scandir(FP.cleaned_up_path_to_source_child_folder) as entries:
            for entry in entries:
                if entry.is_file() and IP.keyword_in_child_document_titles in entry.name:
                    file_count +=1
        
        current_file = 2
        for filename in os.listdir(FP.cleaned_up_path_to_source_child_folder):
            if IP.keyword_in_child_document_titles in filename:
                file_path = FP.cleaned_up_path_to_source_child_folder + "/" + filename
                if os.path.isfile(file_path):
                    FP.file_path_dictionary = FP.handle_source_file_paths(file_path, FP.output_folder_for_child_documents, True)
                    print("__________________________________________________________________________\n\n")
                    print(f"Starting document {current_file} of {file_count}, which is named: '{FP.file_path_dictionary["source_document_file_name_with_extension"]}'")
                    PROC.process_document(IP.step,FP.file_path_dictionary)
            
                current_file +=1
                print(f"...done with '{FP.file_path_dictionary["source_document_file_name_with_extension"]}'.")

if 'STOP GLOBAL TIMER':
    total_elapsed_time = time.time() - total_start_time

    hours = int(total_elapsed_time // 3600)
    minutes = int((total_elapsed_time % 3600) // 60)
    seconds = int(total_elapsed_time % 60)
    milliseconds = int((total_elapsed_time - int(total_elapsed_time)) * 1000)

    print(f"\nTotal runtime for all processes: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} (hh:mm:ss.mmm)")
    print("\n")    