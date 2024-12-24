from datetime import datetime
from pathlib import Path
from queue import Queue
from random import randint
from threading import Thread
from time import sleep

from PyQt6.QtWidgets import QApplication

import broadbandbug.library.files as files
from broadbandbug.gui.graph_windows import MergedGraphWindow, UnmergedGraphWindow
from broadbandbug.library.classes import Reading
from broadbandbug.library.constants import RecordingMethod

test_path = Path("./resources")


# Manual test to make sure everything works
def test_graph():
    app = QApplication([])

    # Create a function that adds new data to the graph, to test live updates
    def add_data(q: Queue):
        while True:
            sleep(1)
            q.put(Reading(randint(0, 40), randint(0, 40), datetime.now(), RecordingMethod.SPEEDTEST_CLI))
            q.put(Reading(randint(0, 40), randint(0, 40), datetime.now(), RecordingMethod.BT_WEBSITE))

    queue = Queue()
    thread = Thread(target=add_data, args=(queue,))
    thread.start()

    # Ungrouped plot
    ungrouped_results = files.read_results(test_path / "actual.csv", None, True)
    MergedGraphWindow.run(app, ungrouped_results, queue, None)

    # Grouped plot
    grouped_results = files.read_results(test_path / "artificial.csv", None, False)
    UnmergedGraphWindow.run(app, grouped_results, queue, None)

    # Test limiting by time constraints
    # Ungrouped plot
    time_constraint = (datetime(day=24, month=6, year=2023), datetime(day=30, month=6, year=2023))
    ungrouped_results = files.read_results(test_path / "artificial.csv", time_constraint, True)
    MergedGraphWindow.run(app, ungrouped_results, queue, time_constraint)

    # Grouped plot
    grouped_results = files.read_results(test_path / "artificial.csv", time_constraint, False)
    UnmergedGraphWindow.run(app, grouped_results, queue, time_constraint)

    exit()


if __name__ == "__main__":
    test_graph()
