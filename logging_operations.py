

#__________________________________________________________________________
###########################################################################
# Class to write logging output to files 
# Named 'tee' because it splits the flow of output like a T-shaped pipe, logging to console and file
class Tee: 
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush() # ensures immediate writing

    def flush(self):
        for f in self.files:
            f.flush()