import time as t

class Header():
    '''Class for printing and updating the header.
    '''

    def __init__(self):
        '''initialize class and set defaults
        '''

        with open("header.files", "r") as f:
            self.
        self.name = "Leo Heller"
        self.filename = __file__
        self.update = "Mo Jan  1 00:00:00 0000"


    def head(self):
        '''Print header
        '''

        print("="*30)
        print("={:^30}=").format(self.name)
        print("={:^30}=").format(self.filename)
        print("={:^30}=").format(self.update)

    def update()
        

class Io():
    def __init__(self):
       pass

    def read(filename):
        '''Reads the contents of the file and returns them
        
        Arguments:
            filename {string} -- filename of the file that should be read
        
        Returns:
            string -- contents of the file
        '''
        with open(filename, "r") as f:
            return f.read()

    def write(filename, content):
        '''writes the content to the file
        erases all content in the file before writing.
        If file does not exist it is created
        
        Arguments:
            filename {string} -- filename of the file that should be written to
            content {string} -- text that should be written to the file
        '''
        with open(filename, "w") as f:
            print(str(content), file=f)

