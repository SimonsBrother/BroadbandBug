import broadbandbug.library.plotting as plotting
import broadbandbug.library.files as files

from matplotlib import pyplot

test_path = "resources/actual.csv"
files.ensureFileExists(test_path)


def test_methodPlot():
    results = files.readResults(test_path, None)

    plotting.styleGraph(pyplot)
    plotting.singlePlot(pyplot, results)

    pyplot.legend()
    pyplot.show()
