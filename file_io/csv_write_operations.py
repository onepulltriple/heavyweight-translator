import csv

def write_translation_dict_to_csv_simplified(temp_translation_dict, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file, quotechar='¥', delimiter='¥')

        for full_paragraph_tagged_text_with_preserves in temp_translation_dict:
            csv_writer.writerow([full_paragraph_tagged_text_with_preserves])
        
        csv_writer.writerow(['____'])
        csv_writer_no_line_return = csv.writer(csv_file, lineterminator='')
        csv_writer_no_line_return.writerow(['____'])
