from pathlib import Path

from matplotlib import pyplot as plt

from ..library import plotting
from ..library import files


test_path = Path("/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/resources")
files.ensure_file_exists(test_path)


# Manual test to make sure everything works
def test_graph():
    # Ungrouped plot
    ungrouped_results = files.read_results(test_path / "artificial.csv", None, False)
    plotting.prepare_plot(plt, "Test ungrouped plot")
    plotting.ungrouped_plot(plt, ungrouped_results)
    plt.show()

    # Grouped plot
    grouped_results = files.read_results(test_path / "artificial.csv", None, True)
    plotting.prepare_plot(plt, "Test grouped plot")
    plotting.grouped_plot(plt, grouped_results)
    plt.show()
