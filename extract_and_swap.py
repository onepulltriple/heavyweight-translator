# Function definitions for extraction, deduplication, and swapping
import docx
import constants 
from docx import Document
from itertools import pairwise, zip_longest, tee
from conditions_checks import *

#__________________________________________________________________________
###########################################################################
# Function to extract text elements from a docx file
def extract_or_swap_text_in_docx(
        input_file, 
        step, 
        translation_dict = None, 
        output_docx = None
    ):

    # Read the unmodified input .docx document into memory
    doc = Document(input_file)

    # create an empty list to host the found text elements
    text_elements = []
    
    # Initialize swap counters
    total_swap_count = 0
    total_no_swap_count = 0

    # Create an empty dictionary (later this will probably be deleted)
    translation_dict_with_paragraphs = {}

    # Iterate over full paragraphs in the document to extract or swap text without splitting up by runs
    # This should help to get better translations from deepl
    for paragraph in doc.paragraphs:
        if paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace():
            if step == constants.EXTRACT:
                # use full paragraph text as a key
                if paragraph.text not in translation_dict_with_paragraphs:
                    translation_dict_with_paragraphs[paragraph.text] = {
                        "full_paragraph_translated_text": None,
                        "consolidated_runs": {}
                    }
            if step == constants.SWAP:
                pass#total_swap_count, total_no_swap_count = consolidate_then_extract_or_swap_text_runs(step, paragraph, text_elements, translation_dict, total_swap_count, total_no_swap_count)

    # Iterate over runs in the paragraph to extract or swap text on a consolidated-run basis
    # This should help later to preserve all special formatting

    # We need: the plain text and style of all consolidated runs from this paragraph
    # [[consolidated_run_plain_text_000001,style_000001],[etc.]]
        (
            text_elements, 
            paragraph, 
            total_swap_count, 
            total_no_swap_count
        ) = consolidate_then_extract_or_swap_text_runs(
                step, 
                paragraph, 
                text_elements, # replacement element after old element
                translation_dict_with_paragraphs[paragraph.text], 
                translation_dict, 
                total_swap_count, 
                total_no_swap_count
            )
        

    # for table in doc.tables:
    #     for row in table.rows:
    #         for cell in row.cells:
    #             for paragraph in cell.paragraphs:
    #                 if paragraph.text is not None:
    #                     if step == constants.EXTRACT:
    #                         pass#text_elements = add_to_text_element_list(paragraph, text_elements)
    #                     if step == constants.SWAP:
    #                         pass#total_swap_count, total_no_swap_count = consolidate_then_extract_or_swap_text_runs(step, paragraph, text_elements, translation_dict, total_swap_count, total_no_swap_count)

    # # Iterate over tables in the document and extract text
    # for table in doc.tables:
    #     for row in table.rows:
    #         for cell in row.cells:
    #             for paragraph in cell.paragraphs:
    #                 (
    #                     text_elements, 
    #                     paragraph, 
    #                     total_swap_count, 
    #                     total_no_swap_count
    #                 ) = consolidate_then_extract_or_swap_text_runs(
    #                         step, 
    #                         paragraph, 
    #                         text_elements, 
    #                         translation_dict, 
    #                         total_swap_count, 
    #                         total_no_swap_count
    #                     )
    #             for table in cell.tables:
    #                 for row in table.rows:
    #                     for cell in row.cells:
    #                         for paragraph in cell.paragraphs:
    #                             (
    #                                 text_elements, 
    #                                 paragraph, 
    #                                 total_swap_count, 
    #                                 total_no_swap_count
    #                             ) = consolidate_then_extract_or_swap_text_runs(
    #                                     step, 
    #                                     paragraph, 
    #                                     text_elements, 
    #                                     translation_dict, 
    #                                     total_swap_count, 
    #                                     total_no_swap_count
    #                                 )


    if step == constants.EXTRACT:
        return text_elements

    if step == constants.SWAP:
        # Save the modified document to the output file
        doc.save(output_docx)
        print(f"There were {total_swap_count} swaps and {total_no_swap_count} no-swaps.\n")

#__________________________________________________________________________
###########################################################################
# Function to consolidate and extract text from paragraphs and hyperlinks
# 
def consolidate_then_extract_or_swap_text_runs(
        step, 
        paragraph, 
        text_collecting_list, 
        #translation_dict_with_paragraphs[paragraph.text],
        translation_dict, 
        current_swap_count, 
        current_no_swap_count
    ):

    # Prepare to consolidate text-having runs
    text_consolidator = ""

    # Hold on to last run when needed
    previous_run = None

    # Toggle progress indication (avoids repeating indications)
    print_progress_indication = True

    # Loop over all the runs/hyperlinks in the paragraph
    for current_run_or_hyperlink, next_run_or_hyperlink in pairwise_circular(paragraph.iter_inner_content()):
        #print("type =>", type(current_run_or_hyperlink))

        # Skip pictures or other non-text-having objects
        if not current_run_or_hyperlink.text:
            previous_run = current_run_or_hyperlink
            continue

        # Indicate progress
        if (current_swap_count % 1000 == 0
             and current_swap_count != 0
             and print_progress_indication):
            print(f"{current_swap_count} {step} operations...")
            print_progress_indication = False

        # If the current object is a hyperlink
        if isinstance(current_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
            # rename object for clarity
            current_hyperlink = current_run_or_hyperlink
            # don't consolidate, just get the text from each text-having run
            for current_run in current_hyperlink.runs:
                if current_run.text:
                    text_collecting_list, current_run, current_swap_count, current_no_swap_count = extract_or_swap(step, current_run, text_collecting_list, translation_dict, current_swap_count, current_no_swap_count)
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
                # collect this run's text
                text_consolidator += current_run.text
                # dump consolidator into this run and reset
                current_run.text = text_consolidator
                # collect or swap
                text_collecting_list, current_run, current_swap_count, current_no_swap_count = extract_or_swap(step, current_run, text_collecting_list, translation_dict, current_swap_count, current_no_swap_count)
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
                # dump and reset
                current_run.text = text_consolidator
                # collect or swap
                text_collecting_list, current_run, current_swap_count, current_no_swap_count = extract_or_swap(step, current_run, text_collecting_list, translation_dict, current_swap_count, current_no_swap_count)
                # clear the text collector and move on
                text_consolidator = ""                
                previous_run = current_run_or_hyperlink
                continue

            print(f"The text-having run \"{current_run_or_hyperlink.text}\" was not handled.\n")

    return text_collecting_list, paragraph, current_swap_count, current_no_swap_count

#__________________________________________________________________________
###########################################################################
# description
def extract_or_swap(
        step, 
        consolidated_run,
        text_collecting_list,
        #translation_dict_with_paragraphs,
        translation_dict,
        current_swap_count,
        current_no_swap_count
    ):

    if step == constants.EXTRACT:
        text_collecting_list, current_swap_count = add_to_text_collecting_list(consolidated_run, text_collecting_list, current_swap_count)
    if step == constants.SWAP:
        consolidated_run, current_swap_count, current_no_swap_count = swap_run(consolidated_run, translation_dict, current_swap_count, current_no_swap_count)

    return text_collecting_list, consolidated_run, current_swap_count, current_no_swap_count

#__________________________________________________________________________
###########################################################################
# Function to swap in translated text on a per-run basis
def swap_run(
        current_run, 
        translation_dict, 
        current_swap_count, 
        current_no_swap_count
    ):
    
    # if there are line breaks in the current run
    if "\n" in current_run.text:
        original_substrings = []
        translated_substrings = []

        # split apart the original string
        original_substrings = current_run.text.split("\n")

        # find the translations
        for substring in original_substrings:
            result = translation_dict.get(substring)
            if result is not None:
                translated_substrings.append(result)
            else:
                print(f"The text element \"{substring}\" was not found in the translation dictionary's keys.")
        
        # assemble the translated string and swap in
        if len(original_substrings) == len(translated_substrings):
            current_run.text = "\n".join(translated_substrings)
            current_swap_count +=1
        else:
            #print(f"The text element \"{original_substrings}\" was not found in the dictionary's keys.")
            # the above line would print the list in brackets
            current_no_swap_count +=1

    # the current run has no line breaks
    else:
        temp_original = current_run.text
        result = translation_dict.get(current_run.text)
        if result is not None:
            current_run.text = result
            current_swap_count +=1
        else:
            print(f"The text element \"{temp_original}\" was not found in the translation dictionary's keys.")
            current_no_swap_count +=1

    return current_run, current_swap_count, current_no_swap_count

#__________________________________________________________________________
###########################################################################
# Function to add text elements to the list while accommodating line breaks
def add_to_text_collecting_list(
        text_having_object, 
        text_collecting_list,
        translation_dict_with_paragraphs,
        current_swap_count
    ):

    temp_list = text_having_object.text.splitlines(keepends = False) # splits text elements at line breaks
    run_style = text_having_object.style
    for element in temp_list:
        #text_collecting_list.append(element)

        text_collecting_list.append([element,run_style])
        #translation_dict_with_paragraphs.append(element)
        current_swap_count +=1

    return text_collecting_list, current_swap_count

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