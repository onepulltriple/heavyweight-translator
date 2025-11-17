# Function definitions for csv-writing tasks
import csv
import os.path

#__________________________________________________________________________
###########################################################################
# Function to dump the source plain text from the temp_translation dictionary to a csv file
def write_translation_dict_to_csv_simplified(temp_translation_dict, file_path):
    # if os.path.exists(file_path):
    #     print(f"File already exists at '{file_path}'.\nAborting to avoid overwrite...")
    # else:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file, quotechar='¥', delimiter='¥')

            for full_paragraph_tagged_text_with_preserves in temp_translation_dict:
                # Write the full paragraph tagged text
                csv_writer.writerow([full_paragraph_tagged_text_with_preserves])
            
            # Write bogus final line (avoids later attempts to read in None)
            csv_writer.writerow(['____'])
            csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
            csv_writer_no_line_return.writerow(['____'])
