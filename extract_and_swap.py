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
# Argument ordering for functions: translation_dict, paragraph, current_run, variables/counters
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
    total_no_swap_count = 0
    newest_print_progress_threshold = 10


    # PARAGRAPHS ##########################################################
    for paragraph in doc.paragraphs:
        process_paragraph_and_runs_within_it(translation_dict, paragraph, step, total_no_swap_count)
        newest_print_progress_threshold = indicate_progress(translation_dict, step, newest_print_progress_threshold)
        

    # TABLES ##############################################################
    for table in doc.tables:
        process_table_cells(translation_dict, table, step, total_no_swap_count)
        newest_print_progress_threshold = indicate_progress(translation_dict, step, newest_print_progress_threshold)


    # RESULTS #############################################################
    print(f"There were {count_total_operations(translation_dict)} {step} operations.\n")
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
def consolidate_then_extract_or_swap_text_runs(translation_dict, paragraph, step):

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
# def lookup_translations(consolidated_run, translation_dict):

#     # Split apart the source consolidated run into a list of substrings 
#     # (consolidated runs without line breaks become single-item lists)
#     source_substrings_list = consolidated_run.text.split("\n")

#     translated_substrings_list = []

#     # Find the translations
#     for substring in source_substrings_list:
#         result = translation_dict.get(substring)
#         if result is not None:
#             translated_substrings_list.append(result)
#         else:
#             print(f"The text element \"{substring}\" was not found in the translation dictionary's keys.")
    
#     # If all substrings have been found
#     if len(source_substrings_list) == len(translated_substrings_list):
#         # The swap can proceed
#         # (Joining a single-item list of strings returns a string)
#         return "\n".join(translated_substrings_list)
    
#     return None

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
def preserve_paragraph_special_items_with_temp_symbols(paragraph_obj):
    return (paragraph_obj.text
            .replace('\n','<a>') # to preserve newlines in multiline runs
            .replace('\xa0','<b>') # to preserve non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the paragraph level
# def unpreserve_paragraph_translation(full_paragraph_translated_text):
#     return (full_paragraph_translated_text
#             .replace('<a>','\n') # to restore newlines in multiline runs
#             .replace('<b>','\xa0') # to restore non-breaking spaces
#             )

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the run level, which deepl seems to otherwise mess up
def preserve_run_special_items_with_temp_symbols(run_obj):
    return (run_obj.text
            .replace('\n','<a>') # to preserve newlines in multiline runs
            .replace('\xa0','<b>') # to preserve non-breaking spaces
            )

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the run level
# def unpreserve_run_text(run_text):
#     return (run_text
#             .replace('<a>','\n') # to restore newlines in multiline runs
#             .replace('<b>','\xa0') # to restore non-breaking spaces
#             )

#__________________________________________________________________________
###########################################################################
# Function to extract full paragraphs and add them to the translation dictionary
def paragraph_level_extractor(translation_dict, paragraph_obj):
    # Use full paragraph text as a key after changing it to "preserved" format
    full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph_obj)

    # Add it to the translation dictionary
    translation_dict[full_paragraph_plain_text_with_preserves] = {
        "full_paragraph_tagged_text": "",
        "full_paragraph_translated_text_with_preserves": None,
        "full_paragraph_translated_tagged_text_with_preserves": None,
        "full_paragraph_style": paragraph_obj.style.name,
        "full_paragraph_is_to_translate": True,
        "consolidated_runs": {}
    }


#__________________________________________________________________________
###########################################################################
# Function to extract consolidated runs and add them to the translation dictionary
# Adds the cons. run its paragraph's sub-dictionary
def run_level_extractor(translation_dict, paragraph_obj, current_run_obj):
    # if paragraph.text in translation_dict:
    #     return

    run_text = current_run_obj.text

    # Add each consolidated run to the paragraph's sub-dictionary
    if run_text is not None and run_text != "" and not run_text.isspace():
        # Look up the paragraph in the translation dictionary (it must be in its "preserved" format)
        full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph_obj)
        # Create a tag counter for this consolidated run (works out because index = current length consolidated runs sub-dictionary)
        tag_counter = len(translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'])
        # Check if the consolidated run is already present. If not, proceed
        if run_text not in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']:
            # Preserve the consolidated run's special characters
            run_text_with_preserves = preserve_run_special_items_with_temp_symbols(current_run_obj)
            # Make a copy with tags
            tagged_run_text_with_preserves = f"<{tag_counter:02}>{run_text_with_preserves}</{tag_counter:02}>"
            # Add it to the translation dictionary
            translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][run_text_with_preserves] = {
                'cons_run_tagged_text': tagged_run_text_with_preserves,
                'cons_run_translated_text_with_preserves': None,
                'cons_run_translated_tagged_text_with_preserves': None,
                'cons_run_style': current_run_obj.style.name,
                'cons_run_is_to_translate': True
            }

            
            # If the run is of a non-default style
            if current_run_obj.style.name != "Default Paragraph Font":
                # Append it to the paragraph's tagged text with tags
                translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text'] += tagged_run_text_with_preserves
            else: # The run is of the default style
                # Append without tags
                translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text'] += run_text_with_preserves



#__________________________________________________________________________
###########################################################################
# Function to retain special symbols, which deepl seems to otherwise mess up
def paragraph_level_swapper(translation_dict, paragraph_obj, total_no_swap_count):
    # Use full paragraph text as a key after changing it to "preserved" format
    full_paragraph_preserved_text = preserve_paragraph_special_items_with_temp_symbols(paragraph_obj)

    # Attempt to find a translation in the dictionary
    if full_paragraph_preserved_text in translation_dict:
        # If the lookup succeeded, proceed with swap
        full_paragraph_preserved_translation = translation_dict[full_paragraph_preserved_text]['full_paragraph_translated_text']
        #paragraph.text = unpreserve_paragraph_translation(full_paragraph_preserved_translation)
    else:
        print(f"The text element \"{full_paragraph_preserved_text}\" was not found in the translation dictionary's keys.")
        total_no_swap_count +=1
    
    return paragraph_obj, total_no_swap_count

#__________________________________________________________________________
###########################################################################
# Function to extract consolidated runs and add them to the translation dictionary
def run_level_swapper(translation_dict, paragraph_obj, current_run_obj, current_no_swap_count):
    run_text = current_run_obj.text

    # Look up the paragraph in the translation dictionary (it must be in its "preserved" format)
    full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph_obj)

    # Attempt to find a full paragragh translation in the dictionary
    if full_paragraph_plain_text_with_preserves in translation_dict:

        # Use current run text as "inner" key after changing it to "preserved" format
        run_text_with_preserves = preserve_run_special_items_with_temp_symbols(current_run_obj)

        # Attempt to find a translation for the consolidated run in the sub-dictionary








    
        # Swap in full paragraph translated text, keeping preserves

        # Find and replace runs with special formatting in the new paragraph translated text
        # The runs should be used to which is not in the same order!

        # Apply that run's style to the translated segment 


    # # If the lookup succeeded
    # if result is not None:
    #     # Proceed with swap
    #     current_run_preserved_text = translation_dict[full_paragraph_preserved_text]['consolidated_runs'][current_run_preserved_text]['cons_run_translated_text']
    #     current_run = unpreserve_run_text(current_run_preserved_text)
    else:
        print(f"The text element \"{full_paragraph_plain_text_with_preserves}\" was not found in the translation dictionary's keys.")
        current_no_swap_count +=1

    return current_run_obj, current_no_swap_count


#__________________________________________________________________________
###########################################################################
# Function to 
def process_table_cells(translation_dict, table, step, total_no_swap_count):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                process_paragraph_and_runs_within_it(translation_dict, paragraph, step, total_no_swap_count)
            
            # Recursively process any nested tables inside the current cell
            for nested_table in cell.tables:
                process_table_cells(translation_dict, nested_table, step, total_no_swap_count)

#__________________________________________________________________________
###########################################################################
# Function to 
def process_paragraph_and_runs_within_it(translation_dict, paragraph, step, total_no_swap_count): 
    if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
        # PARAGRAPH-LEVEL #################################################
        if step == constants.EXTRACT:
            if preserve_paragraph_special_items_with_temp_symbols(paragraph) in translation_dict:
                return
            paragraph_level_extractor(translation_dict, paragraph)

        if step == constants.SWAP:
            pass#(paragraph, total_no_swap_count) = paragraph_level_swapper(paragraph, translation_dict, total_no_swap_count)

        # RUN-LEVEL #######################################################
        # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
        (paragraph, current_no_swap_count) = consolidate_then_extract_or_swap_text_runs(translation_dict, paragraph, step)
        total_no_swap_count += current_no_swap_count
        

#__________________________________________________________________________
###########################################################################
# Function to 
def indicate_progress(translation_dict, step, newest_print_progress_threshold):
    
    total_op_count = count_total_operations(translation_dict)

    if (total_op_count > newest_print_progress_threshold):
        print(f"{newest_print_progress_threshold} {step} operations...")
        newest_print_progress_threshold += 10

    return newest_print_progress_threshold


#__________________________________________________________________________
###########################################################################
# Function to 
def count_total_operations(translation_dict):
    total_op_count = 0
    for outer_key in translation_dict:
        # Count the paragraph's consolidated runs
        total_op_count += len(translation_dict[outer_key]['consolidated_runs'])
        # Count the paragraph itself
        total_op_count += 1

    return total_op_count
