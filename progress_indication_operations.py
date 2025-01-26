
#__________________________________________________________________________
###########################################################################
# Function to 
def indicate_progress(translation_dict, step, newest_print_progress_threshold):
    
    total_op_count = count_total_operations(translation_dict)

    if (total_op_count > newest_print_progress_threshold):
        print(f"{newest_print_progress_threshold} {step} operations...")
        newest_print_progress_threshold += 1000

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

