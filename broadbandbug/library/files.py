import csv
import json
from datetime import datetime

from broadbandbug.library.classes import Result
from broadbandbug.library.constants import TIME_FORMAT


# Checks whether the file specified exists, making it if it does not.
def makeFile(path: str):
    try:
        path = open(str(path), "r")
        path.close()
        return True
    except FileNotFoundError:
        path = open(str(path), "w")
        path.close()
        return False


def writeResults(csv_path: str, result_obj):
    """
    Records results of a speed test to the csv file at the path specified. May raise any errors from open() statement.
    :param csv_path: path to the csv file to write results to
    :param result_obj: the results to store, as a Result object
    """

    with open(csv_path, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([result_obj.download, result_obj.upload, result_obj.timestamp, result_obj.method])


def readResults(csv_path: str, dt_constraints: tuple):
    """
    Reads the results stored in the file at csv_path. May raise any errors from open() statement.
    :param csv_path: path to csv file to read results from
    :param dt_constraints: a tuple storing two datetime objects to indicate what times to return (from, to)
    :return: a dictionary of results objects, separating different types of bugs
    """

    results_dict = {}

    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)

        # Unpack each row into Result object
        for row in reader:
            result = Result(*row)

            # Convert timestamp to datetime, and check it is in bounds
            timestamp_dt = datetime.strptime(result.timestamp, TIME_FORMAT)
            if dt_constraints[0] <= timestamp_dt <= dt_constraints[1]:

                # If the result type has not yet been encountered, make a new category
                if result.method not in results_dict.keys():
                    # Add the result to the new list when instantiating the new list
                    results_dict[result.method] = [result]

                # Otherwise, add the result to the relevant type
                else:
                    results_dict[result.method].append(result)

    return results_dict


def writePalette(json_path: str, graph_palettes: dict):
    """
    Stores a dictionary of graph color palettes in a json file.
    :param json_path: path to json file to write graph color palettes to
    :param graph_palettes: dictionary of GraphPalette objects to store
    """

    with open(json_path, "w") as json_file:
        json.dump(graph_palettes, json_file, indent=4)


def readPalette(json_path):
    """
    Reads the graph color palettes from a json file.
    :param json_path: path to json file to read from
    :return: dictionary, with each method as a key, to dictionaries each storing download and upload keys, with their
    repective color.
    """

    with open(json_path, "r") as json_file:
        return json.load(json_file)


def resultsWriter(csv_path: str, queue, close_event):
    """
    Opens the csv file specified by csv_path, and writes any new records to it from the queue.
    May raise any errors from open() statement. Adapted from various articles from SuperFastPython.com
    :param csv_path: path to the csv file to write results to
    :param queue: a Queue object that stores Record objects
    :param close_event: an Event object that signifies when the function can end - will continue running until queue empty
    """
    # Open CSV file and initialise writer
    with open(csv_path, "a") as csv_file:
        writer = csv.writer(csv_file)

        # Keep checking if there are results to be stored in the queue to ensure everything added to queue is written,
        # or if the event signifying the end of the program is not triggered
        while queue.qsize() > 0 or not close_event.is_set():
            # Ensure queue is not empty before attempting to get from queue
            if queue.qsize() > 0:
                # Get next result
                result_obj = queue.get()
                # Write next result to csv file
                writer.writerow([result_obj.download, result_obj.upload, result_obj.timestamp, result_obj.method])
                # Flush buffer ti ensure there is no data to be written
                csv_file.flush()
                # Mark task as done since write is now complete
                queue.task_done()
