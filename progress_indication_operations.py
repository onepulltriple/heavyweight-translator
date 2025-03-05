import constants

#__________________________________________________________________________
###########################################################################
# Function to check if a paragraph should be processed
def is_relevant_paragraph(paragraph):
    return paragraph.text is not None and paragraph.text != "" and not paragraph.text.isspace()

#__________________________________________________________________________
###########################################################################
# Function to count paragraphs in a document (i.e. those that will be treated)
def count_paragraphs(doc): 

    count = 0
    for paragraph in doc.paragraphs:
        if is_relevant_paragraph(paragraph):
            count += 1

    for table in doc.tables:
        count += count_table_cells(table)

    return count

#__________________________________________________________________________
###########################################################################
# Function to count paragraphs in tables
def count_table_cells(table): 
    count = 0

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if is_relevant_paragraph(paragraph):
                    count += 1
            
            # Recursively count any nested tables inside the current cell
            for nested_table in cell.tables:
                count += count_table_cells(nested_table)

    return count

#__________________________________________________________________________
###########################################################################
# Function to indicate progress to the user
def indicate_progress(translation_dict, step, newest_print_progress_threshold, print_progress_increment, count_of_relevant_paragraphs):
    
    if step == constants.EXTRACT:
        # How many extraction operations have been completed so far?
        current_op_count = len(translation_dict)

        if (current_op_count > newest_print_progress_threshold):
            percent_complete = round(current_op_count/count_of_relevant_paragraphs*100)

            print(f"{current_op_count} {step} operations performed ({percent_complete}% complete)...")
            newest_print_progress_threshold += print_progress_increment

    if step == constants.SWAP:
        # How many swapping operations have been completed so far?
        current_op_count = count_of_relevant_paragraphs

        if (current_op_count > newest_print_progress_threshold):
            percent_complete = round(current_op_count/len(translation_dict)*100)
            
            print(f"{current_op_count} {step} operations performed ({percent_complete}% complete)...")
            newest_print_progress_threshold += print_progress_increment

    return newest_print_progress_threshold
