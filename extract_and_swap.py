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
from regex_operations import *
from preservation_operations import *
from progress_indication_operations import *
from tagging_operations import *


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
        #write_translation_dict_to_csv(translation_dict, FP.source_language_plain_texts_file_path)
        write_translation_dict_to_csv_simplified(translation_dict, FP.source_language_plain_texts_file_path)
        

    if step == constants.SWAP:
        # Save the modified document to the output file
        doc.save(output_docx)
        print(f"{total_no_swap_count} {step} operations failed.\n")

#__________________________________________________________________________
###########################################################################
# Function to consolidate the text in runs from a paragraph and its hyperlinks
def consolidate_runs(paragraph):

    # Prepare to consolidate text-having runs
    text_consolidator = ""

    # Hold on to last run when needed
    previous_run = None

    index_of_run = -1

    # Loop over all the runs/hyperlinks in the paragraph
    for current_run_or_hyperlink, next_run_or_hyperlink in pairwise_circular(paragraph.iter_inner_content()):
        #print("type =>", type(current_run_or_hyperlink))
        index_of_run += 1

        # Skip pictures or other non-text-having objects
        if not current_run_or_hyperlink.text:
            #current_run_or_hyperlink.text = glyph_tag(index_of_run)
            previous_run = current_run_or_hyperlink
            continue

        # If the current object is a hyperlink
        if isinstance(current_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
            # Rename object for clarity
            current_hyperlink = current_run_or_hyperlink
            # Don't consolidate, just deal with the text from each text-having run

            # This treatment could perhaps be simplified. Maybe hyperlinks don't need consolidation (to be verified)
            for current_run in current_hyperlink.runs:
                if current_run.text:
                    # collect text
                    text_consolidator += current_run.text
                    # dump consolidator into this run
                    current_run.text = text_consolidator                   
                    # clear the text consolidator and move on
                    text_consolidator = ""

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
                # dump consolidator into this run
                current_run.text = text_consolidator                   
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
                current_run.text = ignore_run_tag()
                
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
                current_run.text = ignore_run_tag()
                
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
                current_run.text = ignore_run_tag()
                
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
                # dump consolidator into this run
                current_run.text = text_consolidator
                # clear the text collector and move on
                text_consolidator = ""                
                previous_run = current_run_or_hyperlink
                continue

            print(f"The text-having run \"{current_run_or_hyperlink.text}\" was not handled.\n")

    return paragraph

#__________________________________________________________________________
###########################################################################
# Function to tag and extract text from a paragraph and its hyperlinks
def extract_runs(translation_dict, paragraph_with_cons_runs, full_paragraph_plain_text_with_preserves):

    index_of_run = -1

    # Loop over all the runs/hyperlinks in the paragraph
    for current_run_or_hyperlink in paragraph_with_cons_runs.iter_inner_content():
        index_of_run += 1

        # Create a placeholder for pictures or other non-text-having runs
        if not current_run_or_hyperlink.text:
            # Rename object for clarity
            current_glyph_holder = current_run_or_hyperlink
            # Assign a placeholder to the object's text field
            current_glyph_holder.text = glyph_tag(index_of_run)
            # There is nothing to preserve
            cons_run_plain_text_with_preserves = current_glyph_holder.text
            # Do not add a tag
            cons_run_tagged_text_with_preserves = cons_run_plain_text_with_preserves
            # (style would be Default Paragraph Font)
            cons_run_style = current_glyph_holder.style.name
            
        # Otherwise, if the current object is a hyperlink
        elif isinstance(current_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
            # Rename object for clarity
            current_hyperlink = current_run_or_hyperlink
            # Preserve the consolidated run's special characters
            cons_run_plain_text_with_preserves = preserve_run_special_items_with_temp_symbols(current_hyperlink.text)
            # It needs a tag
            cons_run_tagged_text_with_preserves = hyperlink_tag(cons_run_plain_text_with_preserves, index_of_run)
            # (style would be Hyperlink)
            cons_run_style = "Hyperlink"

        # Otherwise, if the current object is a run    
        elif isinstance(current_run_or_hyperlink, docx.text.run.Run):
            # Rename object for clarity
            current_run = current_run_or_hyperlink
            # If the run is of a non-default style
            if current_run.style.name != "Default Paragraph Font":
                # Preserve the consolidated run's special characters
                cons_run_plain_text_with_preserves = preserve_run_special_items_with_temp_symbols(current_run.text)
                # It needs a tag
                cons_run_tagged_text_with_preserves = styled_run_tag(cons_run_plain_text_with_preserves, index_of_run)
                # (style would be current_run.style.name)
            else: 
                # Preserve the consolidated run's special characters
                cons_run_plain_text_with_preserves = preserve_run_special_items_with_temp_symbols(current_run.text)
                # It does not need a tag
                cons_run_tagged_text_with_preserves = cons_run_plain_text_with_preserves
                # (style would be Default Paragraph Font)
            # Get style
            cons_run_style = current_run.style.name
     
        # Add each consolidated run to the paragraph's sub-dictionary
        # Look up the paragraph in the translation dictionary (key must be in its "preserved" format)
        
        # If the consolidated run is not already in the dictionary
        # and it is a text-having run
        if (cons_run_plain_text_with_preserves not in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']
            and cons_run_plain_text_with_preserves != glyph_tag(index_of_run) 
            and cons_run_plain_text_with_preserves != ignore_run_tag()
            and not cons_run_plain_text_with_preserves.isspace()
            ):
            
            # Add it to the translation dictionary
            translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][cons_run_plain_text_with_preserves] = {
                'cons_run_tagged_text_with_preserves': cons_run_tagged_text_with_preserves,
                'cons_run_translated_tagged_text_with_preserves': None,
                'cons_run_style': cons_run_style,
            }

        # If the run is of a non-default style
        if cons_run_style != "Default Paragraph Font":
            # Append it to the paragraph's tagged text with tags
            translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text_with_preserves'] += cons_run_tagged_text_with_preserves
        else: # The run is of the default style
            # Append without tags
            translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text_with_preserves'] += cons_run_plain_text_with_preserves

    return translation_dict



#__________________________________________________________________________
###########################################################################
# Function to extract full paragraphs and add them to the translation dictionary
def paragraph_level_extractor(translation_dict, paragraph_obj):
    # Use full paragraph text as a key after changing it to "preserved" format
    full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph_obj)

    # Add it to the translation dictionary
    translation_dict[full_paragraph_plain_text_with_preserves] = {
        "full_paragraph_tagged_text_with_preserves": "",
        "full_paragraph_translated_tagged_text_with_preserves": None,
        "full_paragraph_style": paragraph_obj.style.name,
        "consolidated_runs": {}
    }


#__________________________________________________________________________
###########################################################################
# Function to retain special symbols, which deepl seems to otherwise mess up
def paragraph_level_swapper(translation_dict, paragraph_obj, full_paragraph_plain_text_with_preserves, total_no_swap_count):
   
    # Attempt to find a translation in the dictionary
    if full_paragraph_plain_text_with_preserves not in translation_dict:
        print(f"The text element \"{full_paragraph_plain_text_with_preserves}\" was not found in the translation dictionary's keys.")
        total_no_swap_count +=1
        return paragraph_obj, total_no_swap_count
    
    # Get full_paragraph_translated_tagged_text_with_preserves
    full_paragraph_translated_tagged_text_with_preserves = translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_translated_tagged_text_with_preserves']
        
    # Break it into segments
    segments = split_with_tags_and_untagged(full_paragraph_translated_tagged_text_with_preserves)
    
    # # Loop over each segment and use them to populate the paragraph's runs
    # paragraph_obj.clear()
    # for segment in segments:
    #     temp_style = None
    #     # If the run has tags, add its text and style
    #     if contains_numeric_tags(segment):
    #         # Attempt to look up the run in the translation dictionary
    #         segment = remove_numeric_tags(segment)
    #         if segment in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']:
    #             temp_style = translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][segment]['cons_run_style']

    #     segment = unpreserve_run_text(segment)
    #     paragraph_obj.add_run(segment, temp_style)
    
    return paragraph_obj, total_no_swap_count

#__________________________________________________________________________
###########################################################################
# Function to extract consolidated runs and add them to the translation dictionary
def run_level_swap_prep(current_run_obj, current_no_swap_count):
    #current_run_obj.clear()

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
        if step == constants.EXTRACT:
            # PARAGRAPH-LEVEL #################################################
            if preserve_paragraph_special_items_with_temp_symbols(paragraph) in translation_dict:
                return # (do nothing)
            paragraph_level_extractor(translation_dict, paragraph)

            # RUN-LEVEL #######################################################
            # Keep a copy of the paragraph's translation dictionary key
            full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph)
            # Iterate over runs in the paragraph to consolidate them
            paragraph = consolidate_runs(paragraph)
            # Iterate over runs in the paragraph to extract text on a consolidated-run basis
            translation_dict = extract_runs(translation_dict, paragraph, full_paragraph_plain_text_with_preserves)


        if step == constants.SWAP:
            # PARAGRAPH-LEVEL #################################################
            if preserve_paragraph_special_items_with_temp_symbols(paragraph) not in translation_dict:
                return # (do nothing)
            # Keep a copy of the paragraph's translation dictionary key
            full_paragraph_plain_text_with_preserves = preserve_paragraph_special_items_with_temp_symbols(paragraph)
            # Iterate over runs in the paragraph to consolidate them
            paragraph = consolidate_runs(paragraph)

            (paragraph, current_no_swap_count) = paragraph_level_swapper(translation_dict, paragraph, full_paragraph_plain_text_with_preserves, total_no_swap_count)
        
