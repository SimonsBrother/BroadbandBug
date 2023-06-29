from datetime import datetime

from broadbandbug.library.constants import TIME_FORMAT

import matplotlib.pyplot as plt
import matplotlib.dates as md


# Converts date strings to a datetime - this is here for easy future changes
def formatTimeForGraph(string):
    return datetime.strptime(string, TIME_FORMAT)


def styleGraph(graph):
    # Styling
    graph.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(facecolor="#0d0433")
    ax.tick_params(labelcolor="orange")

    graph.gcf().autofmt_xdate()
    xfmt = md.DateFormatter("%d/%m/%Y, %M:%H")
    ax.xaxis.set_major_formatter(xfmt)

    # Labels
    graph.xlabel("Time (day/month/yr, min:hr)", color="white")
    graph.ylabel("Megabits/s", color="white")
    graph.title("Broadband Speed", color="white")


# Plots
def methodPlot(graph, results_dict: dict, palettes: dict):
    """
    Plots each method as a separate line for upload and download
    :param graph: matplotlib pyplot
    :param results_dict: a dictionary that splits the results by method
    :param palettes: a dictionary that splits, by method, the colors (in GraphPalette objects) to be used for each line
    """
    for bug_type in results_dict.keys():
        # Get data needed for each graph
        timestamps = [formatTimeForGraph(result.timestamp) for result in results_dict[bug_type]]
        download_speeds = [result.download for result in results_dict[bug_type]]
        upload_speeds = [result.upload for result in results_dict[bug_type]]

        # Plot download
        graph.plot(timestamps, download_speeds, marker="x", label=f"{bug_type} Download",
                   color=('#' + palettes[bug_type]["download"]), linewidth=2)

        # Plot upload
        graph.plot(timestamps, upload_speeds, marker="+", label=f"{bug_type} Upload",
                   color=('#' + palettes[bug_type]["upload"]), linewidth=1)

        graph.legend()


def singlePlot(graph, results_dict: dict, palette=None):
    """
    Plots a line for download and upload, as a single plot for all methods
    :param graph: matplotlib pyplot
    :param results_dict: a dictionary that splits the results by method
    :param palette: GraphPalette object to be used for lines
    """

    # Initialise lists to store all the data
    timestamps = []
    download_speeds = []
    upload_speeds = []

    # Go through each method's results and add the needed data to lists
    for bug_type in results_dict.keys():
        # Get data needed for each graph
        timestamps += [formatTimeForGraph(result.timestamp) for result in results_dict[bug_type]]
        download_speeds += [result.download for result in results_dict[bug_type]]
        upload_speeds += [result.upload for result in results_dict[bug_type]]

    # Plot download
    graph.plot(timestamps, download_speeds, marker="x", label=f"Download",
               color="#000000", linewidth=2)

    # Plot upload
    graph.plot(timestamps, upload_speeds, marker="+", label=f"Upload",
               color="#ff0000", linewidth=1)

    graph.legend()


if __name__ == "__main__":
    from broadbandbug.library.files import readResults
    from broadbandbug.library.constants import METHOD_SPEEDTESTCLI

    path = "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.csv"
    graphPalettes = {METHOD_SPEEDTESTCLI: {"download": "000000", "upload": "222222"}}

    styleGraph(plt)
    methodPlot(plt, readResults(path), graphPalettes)

    plt.legend()
    plt.show()
