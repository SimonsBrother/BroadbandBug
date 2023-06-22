import os
import sys
from pathlib import Path


# Returns the current directory, allowing for frozen state (i.e., compiled exe)
# NOT MY OWN WORK; SOURCE:
# https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
def getPath():
    path = None
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        path = Path(os.path.dirname(sys.executable))
    elif __file__:
        path = Path(os.path.dirname(__file__))
    return path
