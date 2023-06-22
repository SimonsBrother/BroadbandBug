"""
Simple maintenance script to update .ui_raw files to their python equivalents
"""

# pyuic6 .ui_raw -o .py

import os  # For executing commands on command line
import re  # For getting the name of the GUI from the filename

for file in os.listdir():
    # For each file in the current working directory, use regex to determine which are GUI files, and if so, their name
    match = re.match(r'(.+).ui$', file)

    if match:
        # If the file in consideration is a GUI file, run the command, using the name extracted via regex
        os.system(f"pyuic6 {file} -o {match.group(1)}.py")
