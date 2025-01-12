from docx.enum.style import WD_STYLE_TYPE

#__________________________________________________________________________
###########################################################################
# Function to create a new style
def create_new_style(document, base_style, font_color, font_size, font_name):
    styles = document.styles
    #style.base_style = styles['Normal']
