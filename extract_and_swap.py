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
# Function to extract or swap text elements from a docx file
# PARAGRAPH-LEVEL #########################################################
    # Iterate over full paragraphs in the document to extract or swap text without splitting up by runs
    # This should help to get better translations from deepl
# RUN-LEVEL ###############################################################    
    # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
    # This should help later to preserve all special formatting
def extract_or_swap_text_in_docx(input_file, step, translation_dict = {}, output_docx = None):

    # Read the unmodified input .docx document into memory
    doc = Document(input_file)
    
    # Initialize operation counters
    total_op_count = 0 
    total_no_swap_count = 0
    newest_print_progress_threshold = 1000


    # PARAGRAPHS ##########################################################
    # PARAGRAPH-LEVEL #####################################################
    for paragraph in doc.paragraphs:
        if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
            if step == constants.EXTRACT:
                if paragraph.text not in translation_dict:
                    paragraph_level_extractor(translation_dict, paragraph)

            if step == constants.SWAP:
                pass#(paragraph, total_no_swap_count) = paragraph_level_swapper(paragraph, translation_dict, total_no_swap_count)

            # Indicate progress
            total_op_count += 1
            if (total_op_count > newest_print_progress_threshold):
                print(f"{newest_print_progress_threshold} {step} operations...")
                newest_print_progress_threshold += 1000

        # RUN-LEVEL #######################################################
        # Get current size of translation dict as part of measuring progress
        current_size_of_translation_dict = len(translation_dict)

        # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
        (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
        total_no_swap_count += current_no_swap_count
        
        # Indicate progress
        if len(translation_dict) > current_size_of_translation_dict:
            total_op_count += len(translation_dict) - current_size_of_translation_dict
            if (total_op_count > newest_print_progress_threshold):
                print(f"{newest_print_progress_threshold} {step} operations...")
                newest_print_progress_threshold += 1000
        

    # TABLES ##############################################################
    # PARAGRAPH-LEVEL #####################################################
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
                        if step == constants.EXTRACT:
                            if paragraph.text not in translation_dict:
                                paragraph_level_extractor(translation_dict, paragraph)

                        if step == constants.SWAP:
                            pass#(paragraph, total_no_swap_count) = paragraph_level_swapper(paragraph, translation_dict, total_no_swap_count)

                        # Indicate progress
                        if len(translation_dict) > current_size_of_translation_dict:
                            total_op_count += len(translation_dict) - current_size_of_translation_dict
                            if (total_op_count > newest_print_progress_threshold):
                                print(f"{newest_print_progress_threshold} {step} operations...")
                                newest_print_progress_threshold += 1000

    # RUN-LEVEL ###########################################################
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    # Get current size of translation dict as part of measuring progress
                    current_size_of_translation_dict = len(translation_dict)

                    # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
                    (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
                    total_no_swap_count += current_no_swap_count

                    # Indicate progress
                    if len(translation_dict) > current_size_of_translation_dict:
                        total_op_count += len(translation_dict) - current_size_of_translation_dict
                        if (total_op_count > newest_print_progress_threshold):
                            print(f"{newest_print_progress_threshold} {step} operations...")
                            newest_print_progress_threshold += 1000

                # Same process but another layer deeper to catch paragraphs within tables within cells within tables
                for table in cell.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for paragraph in cell.paragraphs:
                                # Get current size of translation dict as part of measuring progress
                                current_size_of_translation_dict = len(translation_dict)

                                # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
                                (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(step, paragraph, translation_dict)
                                total_no_swap_count += current_no_swap_count

                                # Indicate progress
                                if len(translation_dict) > current_size_of_translation_dict:
                                    total_op_count += len(translation_dict) - current_size_of_translation_dict
                                    if (total_op_count > newest_print_progress_threshold):
                                        print(f"{newest_print_progress_threshold} {step} operations...")
                                        newest_print_progress_threshold += 1000


    # RESULTS #############################################################
    print(f"There were {total_op_count} {step} operations.\n")
    if step == constants.EXTRACT:
        write_dict_to_json(translation_dict, FP.TEMP_translation_dict_file_path)
        write_translation_dict_to_csv(translation_dict, FP.source_language_plain_texts_file_path)

    if step == constants.SWAP:
        # Save the modified document to the output file
        doc.save(output_docx)
        print(f"{total_no_swap_count} {step} operations failed.\n")

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
                        run_level_extractor(translation_dict, paragraph, current_run)

                    if step == constants.SWAP:
                        (current_run, current_no_swap_count) = run_level_swapper(translation_dict, paragraph, current_run, current_no_swap_count)

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
                    run_level_extractor(translation_dict, paragraph, current_run)

                if step == constants.SWAP:
                    (current_run, current_no_swap_count) = run_level_swapper(translation_dict, paragraph, current_run, current_no_swap_count)

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
                    run_level_extractor(translation_dict, paragraph, current_run)

                if step == constants.SWAP:
                    (current_run, current_no_swap_count) = run_level_swapper(translation_dict, paragraph, current_run, current_no_swap_count)

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
    return text_having_object.text.splitlines(keepends = False)

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

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the paragraph level, which deepl seems to otherwise mess up
def preserve_paragraph_special_items_with_temp_symbols(full_paragraph):
    return (full_paragraph.text
            .replace('\n','<01>') # to preserve newlines in multiline runs
            .replace('\xa0','<02>') # to preserve non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the paragraph level
def unpreserve_paragraph_translation(full_paragraph_translated_text):
    return (full_paragraph_translated_text
            .replace('<01>','\n') # to restore newlines in multiline runs
            .replace('<02>','\xa0') # to restore non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the run level, which deepl seems to otherwise mess up
def preserve_run_special_items_with_temp_symbols(run_segment):
    return (run_segment
            #.replace('\n','<01>') # to preserve newlines in multiline runs
            .replace('\xa0','<02>') # to preserve non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the run level
def unpreserve_run_text(run_segment):
    return (run_segment
            #.replace('<01>','\n') # to restore newlines in multiline runs
            .replace('<02>','\xa0') # to restore non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to extract full paragraphs and add them to the translation dictionary
def paragraph_level_extractor(translation_dict, paragraph):
    # Use full paragraph text as a key after changing it to "preserved" format
    full_paragraph_plain_text_keeping_line_breaks = preserve_paragraph_special_items_with_temp_symbols(paragraph)
    # Add it to the translation dictionary
    translation_dict[full_paragraph_plain_text_keeping_line_breaks] = {
        "full_paragraph_translated_text": None,
        "full_paragraph_style": paragraph.style.name,
        "full_paragraph_is_to_translate": True,
        "consolidated_runs": {}
    }


#__________________________________________________________________________
###########################################################################
# Function to extract consolidated runs and add them to the translation dictionary
# Adds the cons. run its paragraph's sub-dictionary
def run_level_extractor(translation_dict, paragraph, current_run):
    consolidated_run_split_at_line_breaks = split_consolidated_run_at_line_breaks(current_run)
    
    # Add each consolidated run to the paragraph's sub-dictionary
    for run_segment in consolidated_run_split_at_line_breaks:
        if run_segment is not None and run_segment != "" and not run_segment.isspace():
            # Look up the paragraph in the translation dictionary (it must be in its "preserved" format)
            full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph)
            if run_segment not in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']:
                # Preserve the consolidated run's special characters
                run_segment_with_preserves = preserve_run_special_items_with_temp_symbols(run_segment)
                # Add it to the translation dictionary
                translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][run_segment_with_preserves] = {
                    'cons_run_translated_text': None,
                    'cons_run_style': current_run.style.name,
                    'cons_run_is_to_translate': True
                }

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols, which deepl seems to otherwise mess up
def paragraph_level_swapper(paragraph, translation_dict, total_no_swap_count):
    # Use full paragraph text as a key after changing it to "preserved" format
    full_paragraph_preserved_text = preserve_paragraph_special_items_with_temp_symbols(paragraph)

    # Attempt to find a translation in the dictionary
    if full_paragraph_preserved_text in translation_dict:
        # If the lookup succeeded, proceed with swap
        full_paragraph_preserved_translation = translation_dict[full_paragraph_preserved_text]['full_paragraph_translated_text']
        paragraph.text = unpreserve_paragraph_translation(full_paragraph_preserved_translation)
    else:
        print(f"The text element \"{full_paragraph_preserved_text}\" was not found in the translation dictionary's keys.")
        total_no_swap_count +=1
    
    return paragraph, total_no_swap_count

#__________________________________________________________________________
###########################################################################
# Function to extract consolidated runs and add them to the translation dictionary
def run_level_swapper(translation_dict, paragraph, current_run, current_no_swap_count):
    # Use full paragraph text as "outer" key after changing it to "preserved" format
    full_paragraph_preserved_text = preserve_paragraph_special_items_with_temp_symbols(paragraph)

    # Use current run text as "inner" key after changing it to "preserved" format
    current_run_preserved_text = preserve_run_special_items_with_temp_symbols(current_run.text)

    # Attempt to find a translation in the dictionary
    if full_paragraph_preserved_text in translation_dict:
        pass
        # Swap in full paragraph translated text, keeping preserves

        # Find and replace runs with special formatting in the new paragraph translated text
        # The runs should be used to which is not in the same order!

        # Apply that run's style to the translated segment 


    # # If the lookup succeeded
    # if result is not None:
    #     # Proceed with swap
    #     current_run_preserved_text = translation_dict[full_paragraph_preserved_text]['consolidated_runs'][current_run_preserved_text]['cons_run_translated_text']
    #     current_run = unpreserve_run_text(current_run_preserved_text)
    # else:
    #     print(f"The text element \"{current_run_preserved_text}\" was not found in the translation dictionary's keys.")
    #     current_no_swap_count +=1

    return current_run, current_no_swap_count













    # # Attempt to find translations in the dictionary
    # result_of_translation_lookup_attempt = lookup_translations(current_run, translation_dict)
    # # If the lookup succeeded
    # if (result_of_translation_lookup_attempt is not None):
    #     # Proceed with swap
    #     current_run.text = result_of_translation_lookup_attempt
    # else:
    #     current_no_swap_count +=1