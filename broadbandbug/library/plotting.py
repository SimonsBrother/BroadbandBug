from datetime import datetime

from broadbandbug.library.constants import TIME_FORMAT

from matplotlib import pyplot as plt, ticker
import matplotlib.dates as md


# TODO: go through this again after everything else, check documentation and hints exist where appropriate




def styleGraph(graph):
    # Styling
    fig, ax = plt.subplots(facecolor="#0d0433")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))  # This is easiest to count, I think
    ax.tick_params(axis='both', which='minor', length=4, color='w')
    ax.tick_params(axis='both', which='major', length=7, color='w')
    ax.tick_params(labelcolor="orange")

    #ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x: round(x, 2)))

    graph.gcf().autofmt_xdate()
    xfmt = md.DateFormatter("%d/%m/%Y, %H:%M")  # TODO use constants once its changed
    ax.xaxis.set_major_formatter(xfmt)

    # Labels
    graph.xlabel("Time (day/month/yr, hr:min)", color="white")
    graph.ylabel("Megabits/s", color="white")
    graph.title("Broadband Speed", color="white")  # TODO: custom title


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


def singlePlot(graph, results_dict: dict):
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
        download_speeds += [float(result.download) for result in results_dict[bug_type]]
        upload_speeds += [float(result.upload) for result in results_dict[bug_type]]

    # Plot download
    graph.plot(timestamps, download_speeds, marker="x", label=f"Download",
               color="#000000", linewidth=2)

    # Plot upload
    graph.plot(timestamps, upload_speeds, marker="+", label=f"Upload",
               color="#ff0000", linewidth=1)

    graph.legend()


if __name__ == "__main__":
    from broadbandbug.library.files import read_results

    path = "../tests/resources/actual.csv"

    styleGraph(plt)
    singlePlot(plt, read_results(path, (datetime.min, datetime.max)))

    plt.show()
