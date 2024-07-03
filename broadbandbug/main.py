import os
import sys
from pathlib import Path
from queue import Queue
from threading import Event
import concurrent.futures as futures

from library.files import results_writer

# TODO fully implement GUI
# TODO make and check methods
# TODO put everything together in main


# TODO double check this, explain why its here
def get_current_dir():
    """ NOT MY OWN WORK.
    SOURCE: https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
    :return: the current directory, allowing for frozen state (i.e., compiled exe)
    """
    path = None
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        path = Path(os.path.dirname(sys.executable))
    elif __file__:
        path = Path(os.path.dirname(__file__))
    return path


# Get locations of needed files (in "data" directory of same directory as program)
wd = get_current_dir()
results_path = str(wd.joinpath("data", "results.csv"))

# Ensure data directory exists (no need to check if results file exists, it is created if needed when opened for writing below)

# Initialise variables
max_recorders = 5

results_queue = Queue()
close_event = Event()

recorders = {}

# Start ThreadPoolExecutor, with max_recorders + 1 to allow for results writer thread
with futures.ThreadPoolExecutor(max_recorders + 1) as threadpool_exe:

    writer_future = threadpool_exe.submit(results_writer, results_path, results_queue, close_event)

    # Prepare GUI TODO
    # Run GUI - program will pause until its closed

    # Stop results writer
    close_event.set()

    # Stop running recorders
    for recorder in list(recorders.values()):
        recorder.stopRecording()
