import re
import xml.etree.ElementTree as ET
from file_operations import *
from file_paths import *

#__________________________________________________________________________
###########################################################################
# Function to split a string that includes tags and preserves into several segments
# def split_with_tags_and_untagged(tagged_text_with_preserves):
#     # First, fix any broken tags
#     #tagged_text_with_preserves = fix_broken_tags(tagged_text_with_preserves)

#     # This regular expression will capture both tagged and untagged text
#     # It will match all tags except <a> and <b>, which are not tags but preserves
#     pattern = r'(<\d+>.*?</\d+>)|([^<]+)' 

#     segments = []
#     for match in re.finditer(pattern, tagged_text_with_preserves):
#         # If the match is a tagged segment, add it to the list
#         if match.group(1):
#             segments.append(match.group(1))
#         # If the match is untagged, add it to the list as well
#         elif match.group(2):
#             segments.append(match.group(2))

#     return segments


# def split_with_tags_and_untagged(input_str):
#     # Regular expression pattern to match tags and text
#     pattern = r'(<[^>]+>|[^<]+)'
    
#     # Using re.findall to find all matches for tags and text segments
#     segments = re.findall(pattern, input_str)
    
#     # Join the results to form a list of segments
#     return [segment for segment in segments if segment.strip()]
#     #return segments


def split_with_tags_and_untagged(input_str):
    
    temp = f"<?xml version=\"1.0\"?><paragraph>{input_str}</paragraph>"
    save_to_text_file(temp_xml_debug, temp)

    root = ET.fromstring(
        f"<?xml version=\"1.0\"?><paragraph>{input_str}</paragraph>"
        )

    # create a list
    chase = []
    # first collect root text, if it is there
    if root.text is not None:
        chase.append(root.text)
    # loop over the elements inside root
    for child in root:
        # collect their text 
        chase.append(child.text)
        # and tail, if present
        if child.tail:
            chase.append(child.tail)

        #if child.attrib:

    

    chase2 = chase
    return ""


#__________________________________________________________________________
###########################################################################
# Function to repair tags that were broken during translation
def fix_broken_tags(input_string):
    # Regular expression patterns to identify broken tags
    broken_open_tag_pattern = r'(<\d+)(?!>)'  # Broken opening numeric tags like <01
    broken_non_numeric_open_tag_pattern = r'(<[a-zA-Z])([^>]+)?(?!>)'  # Broken opening tags like <a
    broken_close_tag_pattern = r'</([a-zA-Z0-9]+)(?!>)'  # Broken closing tags like </a or </01

    # Check if there are any broken tags in the string
    if re.search(broken_open_tag_pattern, input_string) or \
       re.search(broken_non_numeric_open_tag_pattern, input_string) or \
       re.search(broken_close_tag_pattern, input_string):
        
        # If broken tags are found, fix them:
        # Fix broken opening numeric tags like <01 to <01>
        input_string = re.sub(broken_open_tag_pattern, r'\1>', input_string)

        # Fix broken opening non-numeric tags like <a to <a>
        input_string = re.sub(broken_non_numeric_open_tag_pattern, r'\1>', input_string)

        # Fix broken closing tags like </01 to </01>
        input_string = re.sub(broken_close_tag_pattern, r'</\1>', input_string)

    # Return the fixed (or unchanged) string
    return input_string

#__________________________________________________________________________
###########################################################################
# Function to 
def contains_numeric_tags(input_string):
    # Regular expression to match numeric tags (e.g., <01>, </01>, <02>, </02>, etc.)
    opening_pattern = r'<\d+>'  # Matches opening numeric tags like <01>, <02>, etc.
    closing_pattern = r'</\d+>'  # Matches closing numeric tags like </01>, </02>, etc.
    
    # Check if the input string contains either an opening or closing numeric tag
    if re.search(opening_pattern, input_string) or re.search(closing_pattern, input_string):
        return True
    return False

#__________________________________________________________________________
###########################################################################
# Function to 
def remove_numeric_tags(input_string):
    # Regular expression to match only numeric tags (e.g., <01>, </01>, <02>, </02>, etc.)
    pattern = r'<\d+>'  # Matches opening numeric tags like <01>, <02>, etc.
    closing_pattern = r'</\d+>'  # Matches closing numeric tags like </01>, </02>, etc.

    # Use re.sub to replace all matching numeric tags with an empty string
    input_string = re.sub(pattern, '', input_string)
    input_string = re.sub(closing_pattern, '', input_string)
    
    return input_string