import broadbandbug.library.plotting as plotting
import broadbandbug.library.files as files
from broadbandbug.library.constants import METHOD_SPEEDTESTCLI
from broadbandbug.library.classes import GraphPalette

from matplotlib import pyplot

test_path = "test.csv"
files.makeFile(test_path)
graphPalettes = {METHOD_SPEEDTESTCLI: GraphPalette("orange", "grey")}


def test_methodPlot():
    results = files.readResults(test_path)

    plotting.styleGraph(pyplot)
    plotting.methodPlot(pyplot, results, graphPalettes)

    pyplot.legend()
    pyplot.show()
