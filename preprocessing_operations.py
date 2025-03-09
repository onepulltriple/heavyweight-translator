import re

#__________________________________________________________________________
###########################################################################
# Function to replace problematic elements of a large string
def regex_replacements(original_content):
    #pattern = r"<run (\w*)=[\"‘'’](\d*)[\"‘'’](/?)>"

    preprocessed_content = re.sub(r"[‘’]", r'"', original_content)
    preprocessed_content = re.sub(r"<run (\w*)=[\"‘'’](\d*)[\"‘'’](/?)>", r'<run \1="\2"\3>', preprocessed_content)

    return preprocessed_content