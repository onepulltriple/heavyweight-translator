import re
import input_parameters as IP

#__________________________________________________________________________
###########################################################################
# Function to replace problematic elements of a large string
def regex_replacements(original_content):

    preprocessed_content = re.sub(r'[‘’]', r'"', original_content)
    preprocessed_content = re.sub(r"<run (\w*) ?=[\"‘'’“](\d*)[\"‘'’”] ?(/?) ?>", r'<run \1="\2"\3>', preprocessed_content)
    preprocessed_content = re.sub(r"<(\w*)/ >", r'<\1/>', preprocessed_content)
    preprocessed_content = re.sub(r"& lt;", r'&lt;', preprocessed_content) # to fix broken less than placeholders
    preprocessed_content = re.sub(r"& gt;", r'&gt;', preprocessed_content) # to fix broken greater than placeholders
    preprocessed_content = re.sub(r"< ?/ ?run ?>", r'</run>', preprocessed_content) # to fix broken closing run tags
    preprocessed_content = re.sub(r"</run\n ?", r'</run>\n', preprocessed_content) # to fix dropp closing run tags
    
    if IP.target_lang_cult == "en-UK":
        preprocessed_content = re.sub(r'consignment', r'shipment', preprocessed_content)
        preprocessed_content = re.sub(r'Consignment', r'Shipment', preprocessed_content)
        preprocessed_content = re.sub(r'contractor', r'subcontractor', preprocessed_content)
        preprocessed_content = re.sub(r'Contractor', r'Subcontractor', preprocessed_content)
        preprocessed_content = re.sub(r'entrepreneur', r'subcontractor', preprocessed_content)
        preprocessed_content = re.sub(r'Entrepreneur', r'Subcontractor', preprocessed_content)
        preprocessed_content = re.sub(r'quotation', r'price agreement', preprocessed_content)
        preprocessed_content = re.sub(r'Quotation', r'Price agreement', preprocessed_content)
        preprocessed_content = re.sub(r'quote', r'price agreement', preprocessed_content)
        preprocessed_content = re.sub(r'Quote', r'Price agreement', preprocessed_content)
        preprocessed_content = re.sub(r' offer', r' price agreement', preprocessed_content)
        preprocessed_content = re.sub(r'Offer ', r'Price agreement ', preprocessed_content)
        preprocessed_content = re.sub(r'tariff', r'rate', preprocessed_content)
        preprocessed_content = re.sub(r'Tariff', r'Rate', preprocessed_content)
        preprocessed_content = re.sub(r'charging point', r'loading point', preprocessed_content)
        preprocessed_content = re.sub(r'Charging point', r'Loading point', preprocessed_content)
        preprocessed_content = re.sub(r'block', r'lock', preprocessed_content)
        preprocessed_content = re.sub(r'blocked', r'locked', preprocessed_content)
        preprocessed_content = re.sub(r'blocking', r'locking', preprocessed_content)
        preprocessed_content = re.sub(r'Block', r'Lock', preprocessed_content)
        preprocessed_content = re.sub(r'Blocked', r'Locked', preprocessed_content)
        preprocessed_content = re.sub(r'Blocking', r'Locking', preprocessed_content)
        preprocessed_content = re.sub(r'mask', r'form', preprocessed_content)
        preprocessed_content = re.sub(r'Mask', r'Form', preprocessed_content)
        preprocessed_content = re.sub(r'town', r'place', preprocessed_content)
        preprocessed_content = re.sub(r'Town', r'Place', preprocessed_content)
        preprocessed_content = re.sub(r'FIBU', r'FINAC', preprocessed_content)
        preprocessed_content = re.sub(r'MRP plan', r'Dispoplan', preprocessed_content)
        preprocessed_content = re.sub(r'MRP Plan', r'Dispoplan', preprocessed_content)
        preprocessed_content = re.sub(r'lorries', r'trucks', preprocessed_content)
        preprocessed_content = re.sub(r'Lorries', r'Trucks', preprocessed_content)
        preprocessed_content = re.sub(r'lorry', r'truck', preprocessed_content)
        preprocessed_content = re.sub(r'Lorry', r'Truck', preprocessed_content)
        preprocessed_content = re.sub(r'third-party tour', r'foreign tour', preprocessed_content)
        preprocessed_content = re.sub(r'Third-party tour', r'Foreign tour', preprocessed_content)
        preprocessed_content = re.sub(r'external tour', r'foreign tour', preprocessed_content)
        preprocessed_content = re.sub(r'External tour', r'Foreign tour', preprocessed_content)

    return preprocessed_content