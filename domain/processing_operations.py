if 'IMPORT LIBRARIES, VARIABLES, AND FILE PATHS':
    import os
    import sys
    import time

    from app import input_parameters as IP
    from domain import constants as CONST
    from domain import extract_and_swap as EXSWAP
    from file_io import dict_operations as DO
    from file_io import file_operations as FO
    from support import logging_operations as LO


def process_document(step, file_path_dictionary):
    if 'START LOGGING':
        logfile = open(
            file_path_dictionary[f"console_log_{step}_file_path"],'w'
        )

        start_time = time.time()

        sys.stdout = LO.Tee(sys.stdout, logfile)
        sys.stderr = LO.Tee(sys.stderr, logfile)

    DO.maint_translation_dict = DO.read_json_dictionary(
        file_path_dictionary["MAINT_translation_dict_file_path"]
    )
    if DO.maint_translation_dict == None: 
        DO.maint_translation_dict = {}

    print(f"Beginning {step} operations...")

    if step == CONST.EXTRACT:
        EXSWAP.extract_or_swap_text_in_docx(file_path_dictionary, step)

    if step == CONST.SWAP:
        temp_translation_dict = DO.read_json_dictionary(
            file_path_dictionary["TEMP_translation_dict_file_path"]
        )
        
        if (
            not os.path.isfile(
                file_path_dictionary["source_language_plain_texts_file_path"]
            )
            or temp_translation_dict is None
        ):
            print(
                "No file found at:         "
                f"'{file_path_dictionary["source_language_plain_texts_file_path"]}'"
            )
            print(
                "No dictionary found at:   "
                f"'{file_path_dictionary["TEMP_translation_dict_file_path"]}'"
            )
            print(
                f"Operation date is set to: '{IP.operation_date}'\n"
            )
            print(
                "If the above dates don't match, the operation_date "
                "can be set manually in the input parameters. "
                f"This issue arises when the {CONST.EXTRACT} "
                "step was performed on a previous date."
            )
            print(
                "If the above dates DO match, then it looks like the "
                f"{CONST.EXTRACT} step hasn't been completed yet. "
                f"Perform the {CONST.EXTRACT} step first.\n"
            )
            quit()
        
        if (
            temp_translation_dict is not None 
            and len(temp_translation_dict) > 0
            and (
                IP.allow_multiple_swap_processes_per_day == True
                or not FO.file_created_today(
                    file_path_dictionary["output_document_path_with_datetime"]
                )
            )
        ):

            temp_translation_dict = (
                DO.insert_translations_into_translation_dict(
                    file_path_dictionary["source_language_plain_texts_file_path"], 
                    file_path_dictionary["target_language_translations_file_path"], 
                    file_path_dictionary["preprocessed_translations_file_path"], 
                    file_path_dictionary["TEMP_translation_dict_file_path"],
                )
            )
            DO.write_dict_to_json(
                temp_translation_dict, 
                file_path_dictionary["TEMP_translation_dict_file_path"],
            )
            DO.extend_json_dictionary(
                DO.maint_translation_dict, temp_translation_dict
            )
            DO.write_dict_to_json(
                DO.maint_translation_dict, 
                file_path_dictionary["MAINT_translation_dict_file_path"],
            )
            DO.write_dict_to_json(
                DO.maint_translation_dict, 
                file_path_dictionary["MAINT_translation_dict_file_path_SNAPSHOT"],
            )

            EXSWAP.extract_or_swap_text_in_docx(
                file_path_dictionary, 
                step, 
                DO.maint_translation_dict,
            )


    if 'STOP LOGGING':
        elapsed_time = time.time() - start_time

        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

        print(
            "Process runtime: "
            f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} "
            "(hh:mm:ss.mmm)"
        )

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        logfile.close()