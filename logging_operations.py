

#__________________________________________________________________________
###########################################################################
# Class to write logging output to files 
# Named 'tee' because it splits the flow of output like a T-shaped pipe, logging to console and file
class Tee: 
    # Accepts any number of file-like objects, filters out those that are closed, and stores the rest
    def __init__(self, *files): # the * means variable number accepted
        open_files = []
        for file in files:
            if not file.closed:
                open_files.append(file)
        self.files = open_files

    # Write the given data (string) to every file in self.files
    def write(self, data):
        new_files = []
        for file in self.files:
            if not file.closed:
                file.write(data)
                file.flush() 
                new_files.append(file)
        self.files = new_files

    # Ensure all files flush their buffers and write immediately
    def flush(self):
        for file in self.files:
            if not file.closed:
                file.flush() 
