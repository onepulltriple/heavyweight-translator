def unpreserve_paragraph_translation(full_paragraph_translated_text):
    if full_paragraph_translated_text is not None:
        return (full_paragraph_translated_text
                .replace('<a/>','\n') 
                .replace('<b/>','\xa0') 
                .replace('<c/>','«') 
                .replace('<d/>','»') 
                )


def preserve_run_special_items_with_temp_symbols(run_text):
    return (run_text
            .replace('\n','<a/>') 
            .replace('\xa0','<b/>')
            .replace('<<','<c/>') 
            .replace('>>','<d/>') 
            )


def pre_escape_preservations(run_text):
    return (run_text
            .replace('&','and') 
            .replace('<br>','<br/>') 
            )