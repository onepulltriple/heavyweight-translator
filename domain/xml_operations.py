import re
import xml.etree.ElementTree as ET
from datetime import datetime
from file_io import file_operations as FO
from file_io import file_paths as FP


def split_string_into_list_of_tagged_and_untagged_elements(input_str):
    input_str_with_xml_wrapper = f"<?xml version=\"1.0\" encoding=\"utf-8\" ?><paragraph>{input_str}</paragraph>"

    try:
        root = ET.fromstring(input_str_with_xml_wrapper)
    except Exception as e1:
        try:
            input_str_with_xml_wrapper = re.sub(r"<run (\w*)=\"(\d*)\">(.*)</paragraph>", r'<run \1="\2">\3</run></paragraph>', input_str_with_xml_wrapper)
            root = ET.fromstring(input_str_with_xml_wrapper)
        except Exception as e:
            error_time_stamp = datetime.now().strftime('%H_%M_%S_%f')[:-3]
            xml_debug_file_path = FP.file_path_dictionary["start_of_xml_debug_file_path"] + error_time_stamp + FP.file_path_dictionary["end_of_xml_debug_file_path"]
            FO.make_folder(FP.file_path_dictionary["start_of_xml_debug_file_path"])
            FO.save_to_text_file(xml_debug_file_path, input_str_with_xml_wrapper)
            return f"{FP.file_path_dictionary["start_of_xml_debug_file_path"]}"

    translated_content = []

    if root.text is not None:
        translated_content.append({'text': f"{root.text}"})

    for child in root:
        temp_dict = {}
        
        if child.text is not None:
            temp_dict['text'] = f"{child.text}"
        
        if len(list(child.attrib.keys())) > 0:
            temp_attrib_key = list(child.attrib.keys())[0] 
            
            temp_dict['type'] = f"{temp_attrib_key}" 
            temp_dict['run_index'] = int(child.attrib[temp_attrib_key]) 
            
            translated_content.append(temp_dict)

        if child.tail is not None:
            translated_content.append(
                {
                    'text': f"{child.tail}"
                }
            )

    return translated_content 