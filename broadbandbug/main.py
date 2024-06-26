import os
import sys
from pathlib import Path
from queue import Queue
from threading import Event
import concurrent.futures as futures

from broadbandbug.ui.functional.MainWindow import MainWindow
from broadbandbug.library.files import resultsWriter

from PyQt6.QtWidgets import QApplication


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


# Get locations of needed files (in "data" directory of same directory as program)
wd = getPath()
results_path = str(wd.joinpath("data", "results.csv"))
config_path = str(wd.joinpath("data", "config.json"))

# Ensure data directory exists
try:
    os.mkdir("data")
except OSError:
    pass

# Ensure config file exists
if not os.path.exists(config_path):
    # If config file doesn't exist, create it with default contents
    with open(config_path, "w") as config_file:
        config_file.write("""{
    "Speedtest CLI": {
        "download": "000000",
        "upload": "ff0000"
    },
    "BT Website": {
        "download": "4D22AD",
        "upload": "2A2A2A"
    },
    "Which? Website": {
        "download": "E25241",
        "upload": "5082C7"
    }
}""")

# No need to check if results file exists, it is created if needed when opened for writing below

# Initialise variables
# TODO: Possible bug, recorders don't stop immediately, but may appear to stop immediately, so someone could try and add more recorders than allowed.
max_recorders = 5

results_queue = Queue()
close_event = Event()

recorders = {}

# For testing
# results_path = "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.csv"
# config_path = "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.json"

# Open results file for entire program
with open(results_path, 'a') as results_file:
    # Start ThreadPoolExecutor, with max_recorders + 1 to allow for results writer thread
    with futures.ThreadPoolExecutor(max_recorders + 1) as exe:

        writer_future = exe.submit(resultsWriter, results_path, results_queue, close_event)

        # Prepare GUI
        app = QApplication([])

        window = MainWindow(results_path, config_path, recorders, exe, results_queue, max_recorders)
        window.show()

        app.exec()

        # Stop results writer
        close_event.set()

        # Stop running recorders
        for recorder in list(recorders.values()):
            recorder.stopRecording()
