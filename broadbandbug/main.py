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


# Initialise variables todo replace with config
results_path = "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.csv"
config_path = "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.json"
max_recorders = 10

results_queue = Queue()
close_event = Event()


# Open results file for entire program
with open(results_path, 'a') as results_file:
    # Start ThreadPoolExecutor, with max_recorders + 2 to allow for results writer thread, and GUI
    with futures.ThreadPoolExecutor(max_recorders + 2) as exe:

        writer_future = exe.submit(resultsWriter, results_path, results_queue, close_event)
        # todo implement system to add, remove, and keep track of recorders (possibly labeling submitted threads)

        # futures.wait(recorder_futures, return_when=futures.ALL_COMPLETED)

        # Prepare GUI
        app = QApplication([])

        window = MainWindow(results_path, config_path, exe)
        window.show()

        app.exec()
