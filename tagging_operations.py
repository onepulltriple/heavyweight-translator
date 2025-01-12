# Function definitions for tagging operations

#__________________________________________________________________________
###########################################################################
def ignore_run_tag(index_of_run):
    return f"<run ignore='{index_of_run:02}'/>"

def glyph_tag(index_of_run):
    #return f"<run glyph=\"{index_of_run:02}\"/>"
    return f"<run glyph='{index_of_run:02}'/>"

def styled_run_tag(run_text, index_of_run):
    return f"<run styled='{index_of_run:02}'>{run_text}</run>"

def hyperlink_tag(hyperlink_text, index_of_run):
    return f"<run hyperlink='{index_of_run:02}'>{hyperlink_text}</run>"

def changed_run_tag(run_text, index_of_run):
    return f"<run changed='{index_of_run:02}'>{run_text}</run>"

# def changed_run_tag(run_text, index_of_run, font_color, font_size, font_name):
#     return f"<run changed='{index_of_run:02}' font_color='{font_color}' font_size='{font_size}' font_name='{font_name}'>{run_text}</run>"

