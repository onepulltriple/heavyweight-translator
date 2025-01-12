# Function definitions for conditional checks
import re
import docx

###########################################################################
# Conditions which should cause a dump
def the_current_run_has_an_R_character(current_run):
    # Regular expression pattern for an R character
    r_char = re.compile("[®]") 

    # if the current run contains an R character
    if re.search(r_char, current_run.text):
        return True

    return False


def button_like_formatting_starts_and_ends_in_the_current_run(current_run, text_consolidator):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    # the blank character appears an even number of times in the first run of a new round of collection
    if (len(re.findall(blank_char, current_run.text)) > 0 
        and len(re.findall(blank_char, current_run.text)) % 2 == 0 
        and text_consolidator == ""
        ):
        return True
    
    return False

def button_like_formatting_starts_and_ends_in_the_next_run(next_run_or_hyperlink, text_consolidator):
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
    
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    # the blank character appears an even number of times in the next run and there is a new round of collection
    if (len(re.findall(blank_char, next_run_or_hyperlink.text)) > 0 
        and len(re.findall(blank_char, next_run_or_hyperlink.text)) % 2 == 0 
        and text_consolidator == ""
        ):
        return True
    
    return False


def weird_symbol_bracketed_by_blank_char_starts_in_the_current_run(current_run, next_run_or_hyperlink, text_consolidator):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    # the blank character appears in the first run of a new round of collection
    # and the next run has no text
    if (re.search(blank_char, current_run.text) 
        and text_consolidator == ""
        and there_is_no_text_in_the_next_run(next_run_or_hyperlink)
        ):
        return True
    
    return False


def weird_symbol_bracketed_by_blank_char_ends_in_the_current_run(previous_run, current_run, next_run_or_hyperlink, text_consolidator):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    # the blank character appears in the first run of a new round of collection
    if (re.search(blank_char, current_run.text) 
        and text_consolidator == ""
        # and the next run does have text
        and not there_is_no_text_in_the_next_run(next_run_or_hyperlink)
        # and the last run had no text
        and there_is_no_text_in_the_last_run(previous_run) 
        ):
        return True
    
    return False


def button_like_formatting_starts_in_next_run(next_run_or_hyperlink, text_collector):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False

    # the blank character appears after collection has begun
    if re.search(blank_char, next_run_or_hyperlink.text) and text_collector != "":
        return True
    
    return False


def button_like_formatting_ends_in_this_run(current_run, text_collector):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    # the blank character appears in this run after another blank character has already been collected
    if re.search(blank_char, current_run.text) and re.search(blank_char, text_collector):
        return True
    
    return False


def button_like_formatting_ends_in_the_next_run(next_run_or_hyperlink, text_collector):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False

    # the blank character appears in this run after another blank character has already been collected
    if re.search(blank_char, next_run_or_hyperlink.text) and re.search(blank_char, text_collector):
        return True
    
    return False


def internal_hidden_text_style_has_been_reached(next_run_or_hyperlink):
    # the next run contains text that is of the style TLInternZchn, which is normally hidden
    if next_run_or_hyperlink == None:
        return True
    
    # the next run is of the style TLInternZchn
    if (next_run_or_hyperlink.style.name == "TL Intern Zchn"):
        return True
    
    return False


def the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink):
    # the last run is equal to the first run (circle has closed, i.e. all runs were seen)
    if next_run_or_hyperlink == None:
        return True
    
    # the next run is a hyperlink
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
        return True
    
    return False


def there_is_a_change_of_nature(current_run, next_run_or_hyperlink):
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False

    # the font color changes
    if next_run_or_hyperlink.font.color != current_run.font.color:
        return True
    
    # the style name changes
    if next_run_or_hyperlink.style.name != current_run.style.name:
        return True
    
    # the font size changes
    if next_run_or_hyperlink.font.size != current_run.font.size:
        return True
    
    # the font name changes 
    if next_run_or_hyperlink.font.name != current_run.font.name:
        return True

    return False

def there_WAS_a_change_of_nature(current_run, previous_run_or_hyperlink):
    # the previous run was a hyperlink
    if isinstance(previous_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
        return False
    
    if previous_run_or_hyperlink == None: 
        return False
    
    # the font color has returned to normal (matches the paragraph)
    if current_run.font.color == current_run._parent.style.font.color:
        return False
        
    # the font size has returned to normal (no run-level size applied)
    if current_run.font.size == None:
        return False
        
    # the font name has returned to normal (no run-level name applied)
    if current_run.font.name == None:
        return False

    # the font color changed
    if previous_run_or_hyperlink.font.color != current_run.font.color:
        return True
    
    # the style name changed
    # if previous_run_or_hyperlink.style.name != current_run.style.name:
    #     return True
    
    # the font size changed
    if previous_run_or_hyperlink.font.size != current_run.font.size:
        return True
    
    # the font name changed 
    if previous_run_or_hyperlink.font.name != current_run.font.name:
        return True

    return False

def there_is_no_text_in_the_next_run(next_run_or_hyperlink):
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
    
    if not next_run_or_hyperlink.text: # no text in the next run (i.e. None, not whitespace)
        return True
    
    return False


def there_is_no_text_in_the_last_run(previous_run):
    if previous_run == None: # this check avoids null exceptions
        return False
    
    if isinstance(previous_run, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
    
    if not previous_run.text: # no text in the last run (i.e. None, not whitespace)
        return True
    
    return False

###########################################################################
# Conditions under which to keep collecting
def bogus_change_of_nature_conditions_are_found(previous_run, current_run, next_run_or_hyperlink):
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False
     
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
    
    if isinstance(previous_run, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
       
    # if the style name of the next run is Quote Char and the next run is not just a blank space, 
    # then this shouldn't count as a change of nature
    if (next_run_or_hyperlink.style.name == "Quote Char"
        and not next_run_or_hyperlink.text.isspace()):
        return True
    
    # if the style name of the current run is Quote Char and the last run is not just a blank space, 
    # then this shouldn't count as a change of nature
    if (current_run.style.name == "Quote Char"
        and not current_run.text.isspace()):
        return True
    
    # if the current run has a particular string
    # and the next run starts with a colon
    # then this shouldn't count as a change of nature
    if ((current_run.text == "Achtung"
         or current_run.text == "Hinweis"
         or current_run.text == "Anwendungsfall"
         or current_run.text == "Tipp"
         )
        and next_run_or_hyperlink.text.startswith(":")
    ):
        return True
        
    return False
    

def the_next_run_has_one_or_two_special_characters(next_run_or_hyperlink):
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): # not messing with hyperlinks here
        return False
    
    if not next_run_or_hyperlink.text: # no text in the next run
        return False
    
    # Regular expression pattern for the blank character (which should not contribute towards the character count)
    blank_char = re.compile("(\\xa0)")

    # blank characters should not be handled here, so return false if any are found
    if len(re.findall(blank_char, next_run_or_hyperlink.text)) > 0:
        return False
    
    # whitespace characters should not be handled here, so return false the run is only whitespace characters
    if next_run_or_hyperlink.text.isspace():
        return False
    
    # Regular expression pattern for special German characters
    de_chars = re.compile("[äöüÄÖÜß]") #®
    
    # if the next run has one or two special characters
    # and the overall length is less than two characters
    if((len(re.findall(de_chars, next_run_or_hyperlink.text)) == 1
       or len(re.findall(de_chars, next_run_or_hyperlink.text)) == 2)
       and len(next_run_or_hyperlink.text) <= 2
       ):
        return True
    
    return False


def the_current_run_has_one_or_two_special_characters(current_run):
    # Regular expression pattern for the blank character (which should not contribute towards the character count)
    blank_char = re.compile("(\\xa0)")

    # blank characters should not be handled here, so return false if any are found
    if len(re.findall(blank_char, current_run.text)) > 0:
        return False
    
    # whitespace characters should not be handled here, so return false the run is only whitespace characters
    if current_run.text.isspace():
        return False
    
    # Regular expression pattern for special German characters
    de_chars = re.compile("[äöüÄÖÜß]") #®
    
    # if the current run has one or two special characters
    # and the overall length is less than two characters
    if((len(re.findall(de_chars, current_run.text)) == 1
       or len(re.findall(de_chars, current_run.text)) == 2)
       and len(current_run.text) <= 2
       ):
        return True
    
    return False

def either_has_special_characters(current_run, next_run_or_hyperlink):
    # Regular expression pattern for special German characters
    de_chars = re.compile("[äöüÄÖÜß]") #®

    # if the current run contains special characters
    if re.search(de_chars, current_run.text):
        return True
    
    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False
    
    # if the next run contains special characters
    if re.search(de_chars, next_run_or_hyperlink.text):
        return True

    return False

def button_like_formatting_starts_in_this_run(current_run, next_run_or_hyperlink, text_collector):
    # Regular expression pattern for the blank character
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: # this check avoids null exceptions
        return False

    # the blank character appears in the first run of a new round of collection
    if re.search(blank_char, current_run.text) and text_collector == "":
        return True
    
    return False

def this_run_occurs_within_a_table(current_run):

    if (current_run._parent == None 
       or current_run._parent._parent == None): # this check avoids null exceptions
        return False

    # the run occurs within a paragraph whose parent is a table cell
    if(isinstance(current_run._parent._parent, docx.table._Cell)):
        return True
    
    return False