# Function definitions for csv-writing tasks
import csv
import os.path

#__________________________________________________________________________
###########################################################################
# Function to write a signle column csv to file
def write_single_column_csv(list_to_write, file_path):
    if os.path.exists(file_path):
        print(f"File already exists at '{file_path}'.\nAborting to avoid overwrite...")
    else:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file) # no delimiter specified, single-column file (default would be ',')

            for row in list_to_write[:-1]:
                csv_writer.writerow([row])
            
            csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
            csv_writer_no_line_return.writerow([list_to_write[-1]])


#__________________________________________________________________________
###########################################################################
# Function to dump the source plain text from the translation dictionary to a csv file
def write_translation_dict_to_csv(translation_dict, file_path):
    # if os.path.exists(file_path):
    #     print(f"File already exists at '{file_path}'.\nAborting to avoid overwrite...")
    # else:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='|') 

            for full_paragraph_plain_text_with_preserves in translation_dict:
                # Write the full paragraph plain text
                csv_writer.writerow([full_paragraph_plain_text_with_preserves])

                # Write the full paragraph tagged text
                csv_writer.writerow([
                    translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text_with_preserves']
                    ])
                
                for cons_run_plain_text_with_preserves in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']:
                    # Write the consolidated run plain text
                    csv_writer.writerow([cons_run_plain_text_with_preserves])
                
                    # Write the consolidated run tagged
                    csv_writer.writerow([
                        translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][cons_run_plain_text_with_preserves]['cons_run_tagged_text_with_preserves']
                        ])
            
            # Write bogus final line (avoids later attempts to read in None)
            csv_writer.writerow(['____'])
            csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
            csv_writer_no_line_return.writerow(['____'])

            
#__________________________________________________________________________
###########################################################################
# Function to dump the source plain text from the translation dictionary to a csv file
def write_translation_dict_to_csv_simplified(translation_dict, file_path):
    # if os.path.exists(file_path):
    #     print(f"File already exists at '{file_path}'.\nAborting to avoid overwrite...")
    # else:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='|') 

            for full_paragraph_plain_text_with_preserves in translation_dict:
                # Write the full paragraph plain text
                csv_writer.writerow([full_paragraph_plain_text_with_preserves])

                # Write the full paragraph tagged text
                csv_writer.writerow([
                    translation_dict[full_paragraph_plain_text_with_preserves]['full_paragraph_tagged_text_with_preserves']
                    ])
                
                # for cons_run_plain_text_with_preserves in translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs']:
                #     # Write the consolidated run plain text
                #     csv_writer.writerow([cons_run_plain_text_with_preserves])
                
                #     # Write the consolidated run tagged
                #     csv_writer.writerow([
                #         translation_dict[full_paragraph_plain_text_with_preserves]['consolidated_runs'][cons_run_plain_text_with_preserves]['cons_run_tagged_text_with_preserves']
                #         ])
            
            # Write bogus final line (avoids later attempts to read in None)
            csv_writer.writerow(['____'])
            csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
            csv_writer_no_line_return.writerow(['____'])