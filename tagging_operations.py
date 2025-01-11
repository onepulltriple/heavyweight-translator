# Function definitions for tagging and un-tagging operations

#__________________________________________________________________________
###########################################################################
def ignore_run_tag():
    return f"<run ignore='1'/>"

def glyph_tag(index_of_run):
    #return f"<run glyph=\"{index_of_run:02}\"/>"
    return f"<run glyph='{index_of_run:02}'/>"

def styled_run_tag(run_text, index_of_run):
    return f"<run style='{index_of_run:02}'>{run_text}</run>"

def hyperlink_tag(hyperlink_text, index_of_run):
    return f"<run hyperlink='{index_of_run:02}'>{hyperlink_text}</run>"

#__________________________________________________________________________
###########################################################################

# def untag_ignore_run():
#     return f"<run ignore/>"

# def untag_glyph(index_of_run):
#     #return f"<run glyph=\"{index_of_run:02}\"/>"
#     return f"<run glyph='{index_of_run:02}'/>"

# def untag_styled_run(run_text, index_of_run):
#     return f"<run style='{index_of_run:02}'>{run_text}</run>"

# def untag_hyperlink(hyperlink_text, index_of_run):
#     return f"<run hyperlink='{index_of_run:02}'>{hyperlink_text}</run>"