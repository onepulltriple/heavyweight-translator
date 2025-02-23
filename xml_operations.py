import xml.etree.ElementTree as ET
from file_operations import *
from file_paths import *

#__________________________________________________________________________
###########################################################################
# Function to split a string that includes tags into several segments
def split_string_into_list_of_tagged_and_untagged_elements(input_str):
    
    # Add a wrapper so that an xml interpreter may be used
    input_str_with_xml_wrapper = f"<?xml version=\"1.0\"?><paragraph>{input_str}</paragraph>"
    # Save a copy as an xml file to aid in debugging
    save_to_text_file(temp_xml_debug, input_str_with_xml_wrapper)
    
    # Repair any issues
    input_str_with_xml_wrapper = (input_str_with_xml_wrapper
        # Correct dropped closing brackets  
        .replace("</run </paragraph>","</run></paragraph>")
        .replace("</run</paragraph>","</run></paragraph>")
    )

    # Parse xml string
    root = ET.fromstring(input_str_with_xml_wrapper)

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
            # Collect the INFO 
            temp_attrib_key = list(child.attrib.keys())[0] # there should only be one key
            
            temp_dict['type'] = f"{temp_attrib_key}" # e.g. hyperlink
            temp_dict['run_index'] = int(child.attrib[temp_attrib_key]) # e.g. the hyperlink's index in the paragraph
            
            translated_content.append(temp_dict)

        # and tail, if present
        if child.tail is not None:
            translated_content.append(
                {
                    'text': f"{child.tail}"
                }
            )

    return translated_content 
