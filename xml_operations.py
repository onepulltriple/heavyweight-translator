import xml.etree.ElementTree as ET
from file_operations import *
from file_paths import *
from datetime import datetime

#__________________________________________________________________________
###########################################################################
# Function to split a string that includes tags into several segments
def split_string_into_list_of_tagged_and_untagged_elements(input_str):
    
    # Add a wrapper so that an xml interpreter may be used
    input_str_with_xml_wrapper = f"<?xml version=\"1.0\" encoding=\"utf-8\" ?><paragraph>{input_str}</paragraph>"

    # Repair any foreseeable issues
    input_str_with_xml_wrapper = (input_str_with_xml_wrapper
        #.replace("&lt;br&gt;","&lt;br/&gt;") # close break tags
        #.replace("<br>","&lt;br/&gt;") # close break tags
    )

    # Attempt to parse xml string
    try:
        root = ET.fromstring(input_str_with_xml_wrapper)
    # If failed, write to file path
    except Exception as e:
        # Get time stamp
        error_time_stamp = datetime.now().strftime('%H_%M_%S_%f')[:-3]
        # Assemble file path
        xml_debug_file_path = start_of_xml_debug_file_path + error_time_stamp + end_of_xml_debug_file_path
        # Save a copy as an xml file to aid in debugging
        save_to_text_file(xml_debug_file_path, input_str_with_xml_wrapper)
        return start_of_xml_debug_file_path

    # Create a list
    translated_content = []

    # First collect root text, if it is there
    if root.text is not None:
        translated_content.append({'text': f"{root.text}"})

    # Loop over the elements inside root
    for child in root:
        temp_dict = {}
        
        if child.text is not None:
            # Collect the text 
            temp_dict['text'] = f"{child.text}"
        
        if len(list(child.attrib.keys())) > 0:
            # Collect attribute information
            temp_attrib_key = list(child.attrib.keys())[0] # there should only be one key
            
            temp_dict['type'] = f"{temp_attrib_key}" # e.g. hyperlink
            temp_dict['run_index'] = int(child.attrib[temp_attrib_key]) # e.g. the hyperlink's index in the paragraph
            
            translated_content.append(temp_dict)

        # Collect tail, if present
        if child.tail is not None:
            translated_content.append(
                {
                    'text': f"{child.tail}"
                }
            )

    return translated_content 
