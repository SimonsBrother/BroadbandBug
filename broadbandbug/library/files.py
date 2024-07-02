import csv
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Event

from . import classes
from . import constants


def ensure_file_exists(path: Path | str, is_dir: bool):
    """ Ensure the file at the path provided exists, creating it if it does not. Returns True if it already existed, False if it had to be created. """
    # Convert from string to path if necessary
    if isinstance(path, str):
        path = Path(path)

    exists = path.exists()

    # Create file is it doesn't exist
    if not exists:
        if is_dir:
            path.mkdir()
        else:
            path.touch()

    return exists


def read_results(csv_path: Path | str, time_constraints: tuple[datetime, datetime] | None, group_by_method: bool) -> dict | list:
    """
    Reads the broadband readings stored in the file at csv_path. May raise any errors from open() statement.
    :param csv_path: path to csv file to read broadband readings from.
    :param time_constraints: a tuple storing two datetime objects to indicate what times to return (from, to). Set to None to ignore this constraint.
    :param group_by_method: set to True to group readings by how they were obtained.
    :return: a dict if group_by_method is True, where each key is a method, linked with a list of Reading objects. Otherwise, returns a list of Reading objects.
    """
    # Create data structure for storing Reading objects - group by method name if necessary, otherwise use a simple list
    readings = {method: [] for method in constants.RecordingMethod} if group_by_method else []

    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        row: dict  # Specify row is a dict, to help PyCharm

        # Rather than considering whether to group by method within the for loop, which would be more readable,
        # I have used 2 for loops running similar code, so that the if statement is not re-evaluated repeatedly,
        # which should be slightly faster.
        if group_by_method:
            for row in reader:
                reading = create_reading_from_row(row)
                if include_reading(reading, time_constraints):
                    readings[reading.method].append(reading)

        else:
            for row in reader:
                reading = create_reading_from_row(row)
                if include_reading(reading, time_constraints):
                    readings.append(reading)

    if group_by_method:
        prune_unused_groups(readings)

    # Sort by timestamp, in case the data from csv is out of order
    sort_by_timestamp(readings, group_by_method)

    return readings


# Used by include_reading, implicitly tested by it
def create_reading_from_row(row: dict) -> classes.Reading:
    """ Creates a Reading object from the dict provided - dict must have keys for 'upload', 'download', 'timestamp', and 'method'.
     For use with a method that gets Readings from a file. """
    return classes.Reading(float(row["upload"]),
                           float(row["download"]),
                           classes.Reading.convert_string_to_datetime(row["timestamp"]),
                           constants.RecordingMethod(row["method"]))


# Used by include_reading, implicitly tested by it
def include_reading(reading: classes.Reading, time_constraints: tuple[datetime, datetime] | None):
    """ Checks if the reading passed to this function should be included in a graph, given certain constraints.
    :param reading: the reading to evaluate.
    :param time_constraints: two datetime objects that the constraint timestamp should be within or equal to - alternatively, None indicates no constraints.
    :return: True if the reading data is within the constraints.
    """
    # Check if timestamp check is needed, and if the timestamp is in bounds (because time constraints is checked first,
    # lazy eval will prevent the rest of the statement from evaluating and causing an error.
    return time_constraints is None or time_constraints[0] <= reading.timestamp <= time_constraints[1]


# Used by include_reading, implicitly tested by it
def prune_unused_groups(readings: dict):
    """ Removes groups that have no readings - this looks nicer on the graph. """
    # Get a list of unused methods - an unused method will not have readings in the list
    unused_methods = []
    for method, group_of_readings in readings.items():
        if len(group_of_readings) == 0:
            unused_methods.append(method)

    # Delete each unused key separately, to prevent the readings dict from changing when it is being iterated
    for method in unused_methods:
        readings.pop(method)


# Used by include_reading, implicitly tested by it
def sort_by_timestamp(readings: dict | list, group_by_method: bool):
    """ For ungrouped, sorts all the readings by timestamp, for grouped, sorts all the readings within each group by timestamp.
    For use with a method that gets readings from a file. """
    def sort(reading: classes.Reading):
        return reading.timestamp

    if group_by_method:
        # Sort within each method
        for method in readings.keys():
            readings[method].sort(key=sort)
    else:
        # Sort all readings
        readings.sort(key=sort)


def results_writer(csv_path: Path | str, queue: Queue, close_event: Event):
    """
    Opens the csv file specified by csv_path, and writes any new records to it from the queue.
    May raise any errors from open() statement. Adapted from various articles from SuperFastPython.com
    :param csv_path: path to the csv file to write results to.
    :param queue: a Queue object that stores Record objects.
    :param close_event: an Event object that indicates when to end - will continue running until queue is empty
    """
    # Open CSV file and initialise writer
    with open(csv_path, "a") as csv_file:
        writer = csv.DictWriter(csv_file, classes.Reading.attributes)
        writer.writeheader()

        # Keep checking if there are results to be stored in the queue to ensure everything added to queue is written,
        # or if the event signifying the end of the program is not triggered
        while queue.qsize() > 0 or not close_event.is_set():
            # Ensure queue is not empty before attempting to get from queue
            if queue.qsize() > 0:
                # Get next result
                result_obj = queue.get()
                result_obj: classes.Reading
                # Write next result to csv file
                writer.writerow(result_obj.format_for_csv())
                # Flush buffer to ensure there is no data to be written
                csv_file.flush()
                # Mark task as done since write is now complete
                queue.task_done()
