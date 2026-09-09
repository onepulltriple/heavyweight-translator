import docx
import re


def the_current_run_has_an_R_character(current_run):
    r_char = re.compile("[®]") 

    if re.search(r_char, current_run.text):
        return True

    return False


def button_like_formatting_starts_and_ends_in_the_current_run(
        current_run, text_consolidator
    ):
    blank_char = re.compile("(\\xa0)")

    if (len(re.findall(blank_char, current_run.text)) > 0 
        and len(re.findall(blank_char, current_run.text)) % 2 == 0 
        and text_consolidator == ""
        ):
        return True
    
    return False


def button_like_formatting_starts_and_ends_in_the_next_run(
        next_run_or_hyperlink, text_consolidator
    ):
    if next_run_or_hyperlink == None:
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): 
        return False
    
    blank_char = re.compile("(\\xa0)")

    if (len(re.findall(blank_char, next_run_or_hyperlink.text)) > 0 
        and len(re.findall(blank_char, next_run_or_hyperlink.text)) % 2 == 0 
        and text_consolidator == ""
        ):
        return True
    
    return False


def weird_symbol_bracketed_by_blank_char_starts_in_the_current_run(
        current_run, next_run_or_hyperlink, text_consolidator
    ):
    blank_char = re.compile("(\\xa0)")

    if (re.search(blank_char, current_run.text) 
        and text_consolidator == ""
        and there_is_no_text_in_the_next_run(next_run_or_hyperlink)
        ):
        return True
    
    return False


def weird_symbol_bracketed_by_blank_char_ends_in_the_current_run(
        previous_run, current_run, next_run_or_hyperlink, text_consolidator
    ):
    blank_char = re.compile("(\\xa0)")

    if (re.search(blank_char, current_run.text) 
        and text_consolidator == ""
        and not there_is_no_text_in_the_next_run(next_run_or_hyperlink)
        and there_is_no_text_in_the_last_run(previous_run) 
        ):
        return True
    
    return False


def button_like_formatting_starts_in_next_run(
        next_run_or_hyperlink, text_collector
    ):
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: 
        return False

    if (
        re.search(blank_char, next_run_or_hyperlink.text) 
        and text_collector != ""
    ):
        return True
    
    return False


def button_like_formatting_ends_in_this_run(current_run, text_collector):
    blank_char = re.compile("(\\xa0)")

    if (
        re.search(blank_char, current_run.text) 
        and re.search(blank_char, text_collector)
    ):
        return True
    
    return False


def button_like_formatting_ends_in_the_next_run(
        next_run_or_hyperlink, text_collector
    ):
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: 
        return False

    if (
        re.search(blank_char, next_run_or_hyperlink.text) 
        and re.search(blank_char, text_collector)
    ):
        return True
    
    return False


def internal_hidden_text_style_has_been_reached(next_run_or_hyperlink):
    if next_run_or_hyperlink == None:
        return True
    
    if (next_run_or_hyperlink.style.name == "TL Intern Zchn"):
        return True
    
    return False


def the_last_run_in_the_paragraph_has_been_reached(next_run_or_hyperlink):
    if next_run_or_hyperlink == None:
        return True
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
        return True
    
    return False


def there_is_a_change_of_nature(current_run, next_run_or_hyperlink):
    if next_run_or_hyperlink == None: 
        return False

    if next_run_or_hyperlink.font.color != current_run.font.color:
        return True
    
    if next_run_or_hyperlink.style.name != current_run.style.name:
        return True
    
    if next_run_or_hyperlink.font.size != current_run.font.size:
        return True
    
    if next_run_or_hyperlink.font.name != current_run.font.name:
        return True
    
    if next_run_or_hyperlink.font.hidden != current_run.font.hidden:
        return True

    return False


def there_WAS_a_change_of_nature(current_run, previous_run_or_hyperlink):
    if isinstance(previous_run_or_hyperlink, docx.text.hyperlink.Hyperlink):
        return False
    
    if previous_run_or_hyperlink == None: 
        return False
    
    if current_run.font.color == current_run._parent.style.font.color:
        return False
        
    if current_run.font.size == None:
        return False
        
    if current_run.font.name == None:
        return False
    
    if current_run.font.hidden == None:
        return False

    if previous_run_or_hyperlink.font.color != current_run.font.color:
        return True
       
    if previous_run_or_hyperlink.font.size != current_run.font.size:
        return True
    
    if previous_run_or_hyperlink.font.name != current_run.font.name:
        return True
    
    if previous_run_or_hyperlink.font.hidden != current_run.font.hidden:
        return True

    return False


def there_is_no_text_in_the_next_run(next_run_or_hyperlink):
    if next_run_or_hyperlink == None: 
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): 
        return False
    
    if not next_run_or_hyperlink.text: 
        return True
    
    return False


def there_is_no_text_in_the_last_run(previous_run):
    if previous_run == None: 
        return False
    
    if isinstance(previous_run, docx.text.hyperlink.Hyperlink): 
        return False
    
    if not previous_run.text: 
        return True
    
    return False


def bogus_change_of_nature_conditions_are_found(
        previous_run, current_run, next_run_or_hyperlink
    ):
    if next_run_or_hyperlink == None: 
        return False
     
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): 
        return False
    
    if isinstance(previous_run, docx.text.hyperlink.Hyperlink): 
        return False
       
    if (next_run_or_hyperlink.style.name == "Quote Char"
        and not next_run_or_hyperlink.text.isspace()):
        return True
    
    if (current_run.style.name == "Quote Char"
        and not current_run.text.isspace()):
        return True
    
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
    if next_run_or_hyperlink == None: 
        return False
    
    if isinstance(next_run_or_hyperlink, docx.text.hyperlink.Hyperlink): 
        return False
    
    if not next_run_or_hyperlink.text:
        return False
    
    blank_char = re.compile("(\\xa0)")

    if len(re.findall(blank_char, next_run_or_hyperlink.text)) > 0:
        return False
    
    if next_run_or_hyperlink.text.isspace():
        return False
    
    de_chars = re.compile("[äöüÄÖÜß]") 
    
    if((len(re.findall(de_chars, next_run_or_hyperlink.text)) == 1
       or len(re.findall(de_chars, next_run_or_hyperlink.text)) == 2)
       and len(next_run_or_hyperlink.text) <= 2
       ):
        return True
    
    return False


def the_current_run_has_one_or_two_special_characters(current_run):
    blank_char = re.compile("(\\xa0)")

    if len(re.findall(blank_char, current_run.text)) > 0:
        return False
    
    if current_run.text.isspace():
        return False
    
    de_chars = re.compile("[äöüÄÖÜß]") 
    
    if ((len(re.findall(de_chars, current_run.text)) == 1
       or len(re.findall(de_chars, current_run.text)) == 2)
       and len(current_run.text) <= 2
       ):
        return True
    
    return False


def either_has_special_characters(current_run, next_run_or_hyperlink):
    de_chars = re.compile("[äöüÄÖÜß]") #®

    if re.search(de_chars, current_run.text):
        return True
    
    if next_run_or_hyperlink == None: 
        return False
    
    if re.search(de_chars, next_run_or_hyperlink.text):
        return True

    return False


def button_like_formatting_starts_in_this_run(
        current_run, next_run_or_hyperlink, text_collector
    ):
    blank_char = re.compile("(\\xa0)")

    if next_run_or_hyperlink == None: 
        return False

    if re.search(blank_char, current_run.text) and text_collector == "":
        return True
    
    return False


def this_run_occurs_within_a_table(current_run):

    if (current_run._parent == None 
       or current_run._parent._parent == None): 
        return False

    if(isinstance(current_run._parent._parent, docx.table._Cell)):
        return True
    
    return False