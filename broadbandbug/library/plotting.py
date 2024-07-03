import matplotlib.dates as md
from matplotlib import pyplot as plt, ticker

from . import classes
from . import constants


def prepare_plot(graph, title="Broadband speed"):
    # Styling
    fig, ax = plt.subplots(facecolor="#0d0433")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Add major and minor ticks
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))  # This is easiest to count, I think
    # Style ticks
    ax.tick_params(axis='both', which='minor', length=4, color='w')
    ax.tick_params(axis='both', which='major', length=7, color='w')
    ax.tick_params(labelcolor="orange")

    # Format x-axis for datetime
    graph.gcf().autofmt_xdate()
    xfmt = md.DateFormatter(constants.TIME_FORMAT)
    ax.xaxis.set_major_formatter(xfmt)

    # Labels
    graph.xlabel("Time (day/month/yr hr:min)", color="white")
    graph.ylabel("Megabits/s", color="white")
    graph.title(title, color="white")


# Plots
def ungrouped_plot(graph, readings: list[classes.Reading]):
    """
    Plots a line for download and upload, as a single plot merging data from all recorders
    :param graph: matplotlib pyplot.
    :param readings: a list of Reading objects to plot a graph of.
    """

    # Initialise lists to store all the data
    timestamps = []
    download_speeds = []
    upload_speeds = []

    # Go through each method's results and add the needed data to lists
    for reading in readings:
        # Get data needed for each graph
        timestamps.append(reading.timestamp)
        download_speeds.append(reading.download)
        upload_speeds.append(reading.upload)

    # Plot download
    graph.plot(timestamps, download_speeds, marker="x", label=f"Download",
               color="#000000", linewidth=2)

    # Plot upload
    graph.plot(timestamps, upload_speeds, marker="+", label=f"Upload",
               color="#ff0000", linewidth=1)

    graph.legend()


def grouped_plot(graph, results_dict: dict):
    """
    Plots each method as a separate line for upload and download
    :param graph: matplotlib pyplot
    :param results_dict: a dictionary that splits the results by method
    """
    for bug_type in results_dict.keys():
        # Get data needed for each graph
        timestamps = [reading.timestamp for reading in results_dict[bug_type]]
        download_speeds = [reading.download for reading in results_dict[bug_type]]
        upload_speeds = [reading.upload for reading in results_dict[bug_type]]

        # Plot download
        graph.plot(timestamps, download_speeds, marker="x", label=f"{bug_type.value} Download", linewidth=2)

        # Plot upload
        graph.plot(timestamps, upload_speeds, marker="+", label=f"{bug_type.value} Upload", linewidth=1)

        graph.legend()
