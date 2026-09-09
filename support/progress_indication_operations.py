import sys
from domain import constants as CONST


def is_relevant_paragraph(paragraph):
    return (
        paragraph.text is not None 
        and paragraph.text != "" 
        and not paragraph.text.isspace()
    )


def count_relevant_paragraphs(doc, step): 
    count = 0

    for section in doc.sections:
        for part in (section.header, section.footer):
            for paragraph in part.paragraphs:
                count += count_paragraphs_considering_step(paragraph, step)
            for table in part.tables:
                count += count_table_cells(table, step)

    for paragraph in doc.paragraphs:
        count += count_paragraphs_considering_step(paragraph, step)

    for table in doc.tables:
        count += count_table_cells(table, step)

    return count


def count_paragraphs_considering_step(paragraph, step): 
    if step == CONST.SWAP:
        if is_relevant_paragraph(paragraph):
            return 1
    else:
        return 1

    return 0


def count_table_cells(table, step): 
    count = 0

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if step == CONST.SWAP:
                    if is_relevant_paragraph(paragraph):
                        count += 1
                else:
                    count += 1
            
            for nested_table in cell.tables:
                count += count_table_cells(nested_table, step)

    return count


def indicate_progress(
        translation_dict, 
        step, 
        newest_print_progress_threshold, 
        print_progress_increment, 
        count_of_relevant_paragraphs, 
        current_op_count
    ):
    
    if step == CONST.EXTRACT:
        count_of_relevant_paragraphs += current_op_count
        current_op_count = len(translation_dict)

    if (current_op_count > newest_print_progress_threshold):
        percent_complete = current_op_count/count_of_relevant_paragraphs*100

        print(
            f"{current_op_count} {step} operations performed ("
            f"{percent_complete:.1f}% complete)...",
            file=sys.__stdout__,
        )
        newest_print_progress_threshold += print_progress_increment

    return newest_print_progress_threshold