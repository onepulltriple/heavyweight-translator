# Function definitions for csv-writing tasks
#import csv
#import os.path

# #__________________________________________________________________________
# ###########################################################################
# # Function to write a single column csv to file
# def write_single_column_csv(list_to_write, file_path):
#     if os.path.exists(file_path):
#         print(f"File already exists at '{file_path}'.\nAborting to avoid overwrite...")
#     else:
#         with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
#             csv_writer = csv.writer(csv_file) # no delimiter specified, single-column file (default would be ',')

#             for row in list_to_write[:-1]:
#                 csv_writer.writerow([row])
            
#             csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
#             csv_writer_no_line_return.writerow([list_to_write[-1]])




# #__________________________________________________________________________
# ###########################################################################
# # Function to assemble a dictionary by zipping together two lists
# def zip_to_lists_to_dict(txt_data_01, txt_data_02):
#     new_dict = {}

#     # Check if the number of rows in each file is the same
#     if len(txt_data_01) != len(txt_data_02):
#         print("Error: The counts of rows in the input files are not equal.\n")
#         return None
#     else:
#         # Iterate over both files simultaneously
#         for row_01, row_02 in zip(txt_data_01, txt_data_02, strict=True):
#             if row_01 not in new_dict:
#                 key = row_01
#                 value = row_02

#                 # Store each entry in the dictionary
#                 new_dict[key] = value

#         return new_dict
