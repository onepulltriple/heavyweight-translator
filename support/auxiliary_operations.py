from itertools import pairwise, zip_longest, tee

# Function to extend pairwise to include a "wrap-around" effect 
# Enables recognition of and access to the last run in a paragraph
def pairwise_circular(iterable):
    # "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = tee(iterable)

    # DO NOT REMOVE THIS LINE!! It is required to maintain the "wrap-around" effect
    first_value = next(b, None) 
    #return zip_longest(a, b, fillvalue = first_value)
    return zip_longest(a, b, fillvalue = None)