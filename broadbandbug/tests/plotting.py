from pathlib import Path
from queue import Queue

from PyQt6.QtWidgets import QApplication

import broadbandbug.library.files as files
from broadbandbug.gui.graph_windows import MergedGraphWindow, UnmergedGraphWindow


test_path = Path("./resources")


# Manual test to make sure everything works
def test_graph():
    app = QApplication([])

    # Ungrouped plot
    ungrouped_results = files.read_results(test_path / "artificial.csv", None, False)
    MergedGraphWindow.run(app, ungrouped_results, Queue())

    # Grouped plot
    grouped_results = files.read_results(test_path / "artificial.csv", None, True)
    UnmergedGraphWindow.run(app, grouped_results, Queue())

    # todo test limiting by time constraints

if __name__ == "__main__":
    test_graph()
