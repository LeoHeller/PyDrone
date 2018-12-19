'''
Helper functions
'''


import time as t
import os
import __main__ as main

update = "Sun Sep  9 22:08:04 2018"
name = "Leo Heller"
filename = os.path.basename(main.__file__)


def setupdate():
    '''
    changes the last update date
    '''
    global update
    update = t.ctime()


def head():
    '''
    Print header
    '''

    print("=" * 32)
    print("|{:^30}|".format(name))
    print("|{:^30}|".format(filename))
    print("|{:^30}|".format(update))
    print("=" * 32, end="\n\n")


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
