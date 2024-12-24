# Function definitions for csv-reading tasks
import csv
import os.path
    
#__________________________________________________________________________
###########################################################################
# Function to read in a csv file
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
    
#__________________________________________________________________________
###########################################################################
# Function to read in a single line csv file and effectively ignore commas as delimiters
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
