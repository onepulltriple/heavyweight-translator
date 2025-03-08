

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the paragraph level
def unpreserve_paragraph_translation(full_paragraph_translated_text):
    if full_paragraph_translated_text is not None:
        return (full_paragraph_translated_text
                .replace('<a/>','\n') # to restore newlines in multiline runs
                .replace('<b/>','\xa0') # to restore non-breaking spaces
                #.replace('<c/>','<<') # to restore double left angle brackets
                .replace('<c/>','«') # to restore double left angle brackets
                #.replace('<d/>','>>') # to restore double right angle brackets
                .replace('<d/>','»') # to restore double right angle brackets
                #.replace('&','and') # to 
                #.replace('&lt;br&gt;','<br>') # to restore line break indicators
                )

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the run level, which deepl seems to otherwise mess up
def preserve_run_special_items_with_temp_symbols(run_text):
    return (run_text
            .replace('\n','<a/>') # to preserve newlines in multiline runs
            .replace('\xa0','<b/>') # to preserve non-breaking spaces
            .replace('<<','<c/>') # to preserve double left angle brackets
            .replace('>>','<d/>') # to preserve double right angle brackets
            #.replace('&lt;br&gt;','<e/>') # to preserve line break indicators
            #.replace('&amp;','<e/>') # 
            )

#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the run level, which deepl seems to otherwise mess up
def pre_escape_preservations(run_text):
    return (run_text
            .replace('&','and')
            .replace('<br>','<br/>')
            )