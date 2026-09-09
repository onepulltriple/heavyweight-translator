from itertools import pairwise, zip_longest, tee

def pairwise_circular(iterable):
    a, b = tee(iterable)

    # DO NOT REMOVE THIS LINE!! It's needed to produce the wrap-around effect
    first_value = next(b, None) 
    return zip_longest(a, b, fillvalue = None)