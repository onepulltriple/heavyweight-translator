# Function definitions for extraction, deduplication, and swapping
import docx
import constants 
import file_paths as FP 
from docx import Document
from itertools import pairwise, zip_longest, tee
from conditions_checks import *
from dict_operations import *
from csv_read_operations import *
from csv_write_operations import *

#__________________________________________________________________________
###########################################################################
# Function to extract text elements from a docx file
def extract_or_swap_text_in_docx(input_file, step, output_docx = None):

    # Read the unmodified input .docx document into memory
    doc = Document(input_file)
    
    # Initialize operation counters
    total_op_count = 0 
    total_no_swap_count = 0
    newest_print_progress_threshold = 1000

    # Create an empty dictionary
    translation_dict = {}

    # Iterate over full paragraphs in the document to extract or swap text without splitting up by runs
    # This should help to get better translations from deepl
    for paragraph in doc.paragraphs:
        if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
            if step == constants.EXTRACT:
                if paragraph.text not in translation_dict:
                    # Use full paragraph text as a key
                    translation_dict[paragraph.text] = {
                        "full_paragraph_translated_text": None,
                        "full_paragraph_style": paragraph.style.name,
                        "consolidated_runs": {}
                    }

            # Indicate progress
            total_op_count += 1
            if (total_op_count > newest_print_progress_threshold):
                print(f"{newest_print_progress_threshold} {step} operations...")
                newest_print_progress_threshold += 1000

            if step == constants.SWAP:
                pass#total_swap_count, total_no_swap_count = consolidate_then_extract_or_swap_text_runs(step, paragraph, text_elements, translation_dict, total_swap_count, total_no_swap_count)


    # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
    # This should help later to preserve all special formatting
    # Next we need: the plain text and style of all consolidated runs from this paragraph
    # [[consolidated_run_plain_text_000001,style_000001],[etc.]]
        current_size_of_translation_dict = len(translation_dict)
        (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
        total_no_swap_count += current_no_swap_count
        
        # Indicate progress
        if len(translation_dict) > current_size_of_translation_dict:
            total_op_count += len(translation_dict) - current_size_of_translation_dict
            if (total_op_count > newest_print_progress_threshold):
                print(f"{newest_print_progress_threshold} {step} operations...")
                newest_print_progress_threshold += 1000
        

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
                        if step == constants.EXTRACT:
                            if paragraph.text not in translation_dict:
                                # Use full paragraph text as a key
                                translation_dict[paragraph.text] = {
                                    "full_paragraph_translated_text": None,
                                    "full_paragraph_style": paragraph.style.name,
                                    "consolidated_runs": {}
                                }

                        # Indicate progress
                        if len(translation_dict) > current_size_of_translation_dict:
                            total_op_count += len(translation_dict) - current_size_of_translation_dict
                            if (total_op_count > newest_print_progress_threshold):
                                print(f"{newest_print_progress_threshold} {step} operations...")
                                newest_print_progress_threshold += 1000

                        if step == constants.SWAP:
                            pass#total_swap_count, total_no_swap_count = consolidate_then_extract_or_swap_text_runs(step, paragraph, text_elements, translation_dict, total_swap_count, total_no_swap_count)

    # Iterate over tables in the document and extract text
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    current_size_of_translation_dict = len(translation_dict)
                    (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
                    total_no_swap_count += current_no_swap_count

                    # Indicate progress
                    if len(translation_dict) > current_size_of_translation_dict:
                        total_op_count += len(translation_dict) - current_size_of_translation_dict
                        if (total_op_count > newest_print_progress_threshold):
                            print(f"{newest_print_progress_threshold} {step} operations...")
                            newest_print_progress_threshold += 1000

                for table in cell.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for paragraph in cell.paragraphs:
                                current_size_of_translation_dict = len(translation_dict)
                                (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
                                total_no_swap_count += current_no_swap_count

                                # Indicate progress
                                if len(translation_dict) > current_size_of_translation_dict:
                                    total_op_count += len(translation_dict) - current_size_of_translation_dict
                                    if (total_op_count > newest_print_progress_threshold):
                                        print(f"{newest_print_progress_threshold} {step} operations...")
                                        newest_print_progress_threshold += 1000


    print(f"There were {total_op_count} {step} operations.\n")
    if step == constants.EXTRACT:
        print_dict_to_json(translation_dict, FP.TEMP_translation_dict_file_path)
        write_translation_dict_to_csv(translation_dict, FP.source_language_plain_texts_file_path)
        read_translation_dict_from_csv(FP.source_language_plain_texts_file_path, FP.target_language_translations_file_path, translation_dict)

    if step == constants.SWAP:
        # Save the modified document to the output file
        doc.save(output_docx)
        print(f"{total_no_swap_count} {step} failed.\n")

#__________________________________________________________________________
###########################################################################
# Function to consolidate and extract text from paragraphs and hyperlinks
def consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict):

    # Initialize operation counters
    current_no_swap_count = 0

    # Prepare to consolidate text-having runs
    text_consolidator = ""

    # Hold on to last run when needed
    previous_run = None

    # Loop over all the runs/hyperlinks in the paragraph
    for current_run_or_hyperlink, next_run_or_hyperlink in pairwise_circular(paragraph.iter_inner_content()):
        #print("type =>", type(current_run_or_hyperlink))

        # Skip pictures or other non-text-having objects
        if not current_run_or_hyperlink.text:
            previous_run = current_run_or_hyperlink
            continue

        # If the current object is a hyperlink
        if isinstance(current_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
            # Rename object for clarity
            current_hyperlink = current_run_or_hyperlink
            # Don't consolidate, just deal with the text from each text-having run
            for current_run in current_hyperlink.runs:
                if current_run.text:
                    # collect or swap
                    if step == constants.EXTRACT:
                        consolidated_run_split_at_line_breaks = split_consolidated_run_at_line_breaks(current_run)
                        
                        # Add each consolidated run to the paragraph's sub-dictionary
                        for run_segment in consolidated_run_split_at_line_breaks:
                            if run_segment is not None and run_segment != "" and not run_segment.isspace():
                                if run_segment not in translation_dict[paragraph.text]['consolidated_runs']:
                                    translation_dict[paragraph.text]['consolidated_runs'][run_segment] = {
                                        'cons_run_translated_text': None,
                                        'cons_run_style': current_run.style.name,
                                        'cons_run_is_to_translate': True
                                    }

                    if step == constants.SWAP:
                        # Attempt to find translations in the dictionary
                        result_of_translation_lookup_attempt = lookup_translations(current_run, translation_dict)
                        # If the lookup succeeded
                        if (result_of_translation_lookup_attempt is not None):
                            # Proceed with swap
                            current_run.text = result_of_translation_lookup_attempt
                        else:
                            current_no_swap_count +=1
            previous_run = current_run_or_hyperlink
            continue

        # Otherwise, if the current object is a run    
        elif isinstance(current_run_or_hyperlink, docx.text.run.Run):
            # Rename object for clarity and to avoid mutating the current_run_or_hyperlink
            current_run = current_run_or_hyperlink

            # Conditions under which to collect and dump immediately
            if (the_current_run_has_an_R_character(current_run)
                or button_like_formatting_starts_and_ends_in_the_current_run(current_run, text_consolidator)
                or button_like_formatting_starts_and_ends_in_the_next_run(next_run_or_hyperlink, text_consolidator)
                or weird_symbol_bracketed_by_blank_char_starts_in_the_current_run(current_run, next_run_or_hyperlink, text_consolidator) 
                or weird_symbol_bracketed_by_blank_char_ends_in_the_current_run(previous_run, current_run, next_run_or_hyperlink, text_consolidator) 
                ):
                # collect text
                text_consolidator += current_run.text
                # dump consolidator into this run and reset
                current_run.text = text_consolidator
                # collect or swap
                if step == constants.EXTRACT:
                    consolidated_run_split_at_line_breaks = split_consolidated_run_at_line_breaks(current_run)
                    
                    # Add each consolidated run to the paragraph's sub-dictionary
                    for run_segment in consolidated_run_split_at_line_breaks:
                        if run_segment is not None and run_segment != "" and not run_segment.isspace():
                            if run_segment not in translation_dict[paragraph.text]['consolidated_runs']:
                                translation_dict[paragraph.text]['consolidated_runs'][run_segment] = {
                                    'cons_run_translated_text': None,
                                    'cons_run_style': current_run.style.name,
                                    'cons_run_is_to_translate': True
                                }

                if step == constants.SWAP:
                    # Attempt to find translations in the dictionary
                    result_of_translation_lookup_attempt = lookup_translations(current_run, translation_dict)
                    # If the lookup succeeded
                    if (result_of_translation_lookup_attempt is not None):
                        # Proceed with swap
                        current_run.text = result_of_translation_lookup_attempt
                    else:
                        current_no_swap_count +=1
                # clear the text consolidator and move on
                text_consolidator = ""
                previous_run = current_run_or_hyperlink
                continue
            
            # Conditions under which to keep consolidating
            if (either_has_special_characters(current_run, next_run_or_hyperlink)
                and (the_current_run_has_one_or_two_special_characters(current_run)
                     or the_next_run_has_one_or_two_special_characters(next_run_or_hyperlink))
                ):
                # collect this run's text
                text_consolidator += current_run.text
                # clear this run's text
                current_run.clear()
                if the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink):
                    pass # move on to the code below
                else:
                    previous_run = current_run_or_hyperlink
                    continue # keep consolidating

            if (button_like_formatting_starts_in_this_run(current_run, next_run_or_hyperlink, text_consolidator)  
                or button_like_formatting_ends_in_the_next_run(next_run_or_hyperlink, text_consolidator)         
                ):
                # collect this run's text
                text_consolidator += current_run.text
                # clear this run's text
                current_run.clear()
                if the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink):
                    pass # move on to the code below
                else:
                    previous_run = current_run_or_hyperlink
                    continue # keep consolidating

            if (bogus_change_of_nature_conditions_are_found(previous_run, current_run, next_run_or_hyperlink)         
                ):
                # collect this run's text
                text_consolidator += current_run.text
                # clear this run's text
                current_run.clear()
                if the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink):
                    pass # move on to the code below
                else:
                    previous_run = current_run_or_hyperlink
                    continue # keep consolidating

            # If one of these conditions is met, stop consolidating
            if (the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink)
                  or there_is_no_text_in_the_next_run(next_run_or_hyperlink)
                  or internal_hidden_text_style_has_been_reached(next_run_or_hyperlink)
                  or button_like_formatting_starts_in_next_run(next_run_or_hyperlink, text_consolidator)
                  or button_like_formatting_ends_in_this_run(current_run, text_consolidator)
                  or there_is_a_change_of_nature(current_run, next_run_or_hyperlink)
                ): 
                # collect text
                text_consolidator += current_run.text
                # dump consolidator into this run and reset
                current_run.text = text_consolidator
                # collect or swap
                if step == constants.EXTRACT:
                    consolidated_run_split_at_line_breaks = split_consolidated_run_at_line_breaks(current_run)
                    
                    # Add each consolidated run to the paragraph's sub-dictionary
                    for run_segment in consolidated_run_split_at_line_breaks:
                        if run_segment is not None and run_segment != "" and not run_segment.isspace():
                            if run_segment not in translation_dict[paragraph.text]['consolidated_runs']:
                                translation_dict[paragraph.text]['consolidated_runs'][run_segment] = {
                                    'cons_run_translated_text': None,
                                    'cons_run_style': current_run.style.name,
                                    'cons_run_is_to_translate': True
                                }

                if step == constants.SWAP:
                    # Attempt to find translations in the dictionary
                    result_of_translation_lookup_attempt = lookup_translations(current_run, translation_dict)
                    # If the lookup succeeded
                    if (result_of_translation_lookup_attempt is not None):
                        # Proceed with swap
                        current_run.text = result_of_translation_lookup_attempt
                    else:
                        current_no_swap_count +=1
                # clear the text collector and move on
                text_consolidator = ""                
                previous_run = current_run_or_hyperlink
                continue

            print(f"The text-having run \"{current_run_or_hyperlink.text}\" was not handled.\n")

    return paragraph, current_no_swap_count


#__________________________________________________________________________
###########################################################################
# Function to lookup translated text on a per-consolidated_run basis
# Also reassembles translated strings that were broken apart because their source text contained line breaks
def lookup_translations(consolidated_run, translation_dict):

    # Split apart the source consolidated run into a list of substrings 
    # (consolidated runs without line breaks become single-item lists)
    source_substrings_list = consolidated_run.text.split("\n")

    translated_substrings_list = []

    # Find the translations
    for substring in source_substrings_list:
        result = translation_dict.get(substring)
        if result is not None:
            translated_substrings_list.append(result)
        else:
            print(f"The text element \"{substring}\" was not found in the translation dictionary's keys.")
    
    # If all substrings have been found
    if len(source_substrings_list) == len(translated_substrings_list):
        # The swap can proceed
        # (Joining a single-item list of strings returns a string)
        return "\n".join(translated_substrings_list)
    
    return None

#__________________________________________________________________________
###########################################################################
# Function to break text elements at line breaks
# Runs must be split on line breaks (line breaks are used as delimiters)
# e.g. bullet lists where one bullet point spans multiple lines
def split_consolidated_run_at_line_breaks(text_having_object):
    # This line kept in case further manipulation becomes necessary
    temp_list = text_having_object.text.splitlines(keepends = False)

    return temp_list

#__________________________________________________________________________
###########################################################################
# Function to extend pairwise to include a "wrap-around" effect 
# This is done to be able to recognize and access the last run in a paragraph
def pairwise_circular(iterable):
    # "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = tee(iterable)
    first_value = next(b, None) # DO NOT REMOVE THIS LINE!!
    #return zip_longest(a, b, fillvalue = first_value)
    return zip_longest(a, b, fillvalue = None)