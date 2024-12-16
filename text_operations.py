# Function definitions for text-related tasks
import csv
import os.path

#_____________________________________________________________________________________________________________________________#
# Function to read a single-column text file and return a list of values
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return [line.strip() for line in file]
    
#_____________________________________________________________________________________________________________________________#    
# Write a query to an output SQL file
def write_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8-sig') as output_file:
        output_file.write(text)

#_____________________________________________________________________________________________________________________________#
# read in a csv file
def read_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)

            csv_data = []
            #counter=0
            for row in csv_reader:
                csv_data.append(row[0].strip())    #.replace("\'","\'\'")
                #counter+=1

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None
    
#_____________________________________________________________________________________________________________________________#
# read in a single line csv file and effectively ignore commas as delimiters
def read_csv_keeping_full_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)

            csv_data = []
            
            for row in csv_reader:
                # Join the row back into a single string with commas 
                # Lines wrapped in quotes are already considered to have length = 1
                full_line = ''
                for i in range(len(row)):
                    if i > 0:
                        full_line += ','
                    full_line += row[i]

                # Append to the array
                csv_data.append(full_line.strip())  

            return csv_data
        
    except FileNotFoundError:
        print(f"No file found at '{file_path}'.")
        return None

#_____________________________________________________________________________________________________________________________#
# what to write, where to write it
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