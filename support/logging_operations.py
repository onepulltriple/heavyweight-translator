class Tee: 
    def __init__(self, *files):
        open_files = []
        for file in files:
            if not file.closed:
                open_files.append(file)
        self.files = open_files


    def write(self, data):
        new_files = []
        for file in self.files:
            if not file.closed:
                file.write(data)
                file.flush() 
                new_files.append(file)
        self.files = new_files


    def flush(self):
        for file in self.files:
            if not file.closed:
                file.flush() 
