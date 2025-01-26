
#__________________________________________________________________________
###########################################################################
# Function to retain special symbols at the paragraph level, which deepl seems to otherwise mess up
def preserve_paragraph_special_items_with_temp_symbols(paragraph_obj):
    return (paragraph_obj.text
            .replace('\n','<a/>') # to preserve newlines in multiline runs
            .replace('\xa0','<b/>') # to preserve non-breaking spaces
            .replace('<<','<c/>') # to preserve double left angle brackets
            .replace('>>','<d/>') # to preserve double right angle brackets
            )

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
                .replace('&','and') # to restore double right angle brackets
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
            )

#__________________________________________________________________________
###########################################################################
# Function to restore special symbols at the run level
def unpreserve_run_text(run_text):
    if run_text is not None:
        return (run_text
                .replace('<a/>','\n') # to restore newlines in multiline runs
                .replace('<b/>','\xa0') # to restore non-breaking spaces
                #.replace('<c/>','<<') # to restore double left angle brackets
                .replace('<c/>','«') # to restore double left angle brackets
                #.replace('<d/>','>>') # to restore double right angle brackets
                .replace('<d/>','»') # to restore double right angle brackets
                .replace('&','and') # to restore double right angle brackets
                )