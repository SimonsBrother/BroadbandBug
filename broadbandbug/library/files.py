""" Contains most functions related to file handling, including creation, reading, and filtering. """
import csv
from datetime import datetime
from pathlib import Path

from . import classes
from . import constants


def ensure_file_exists(path: Path | str, is_dir: bool):
    """ Ensure the file at the path provided exists, creating it if it does not.
    Returns True if it already existed, False if it had to be created. """
    # Convert from string to path if necessary
    if isinstance(path, str):
        path = Path(path)

    exists = path.exists()
    print(path)
    print(exists)

    # Create file or directory is it doesn't exist
    if not exists:
        if is_dir:
            path.mkdir()
        else:
            path.touch()

    return exists


def read_results(csv_path: Path | str, time_constraints: tuple[datetime, datetime] | None, merge_methods: bool) -> dict | list:
    """
    Reads the broadband readings stored in the file at csv_path.
        May raise any errors from an open() statement, or if csv_path refers to a file that is not a CSV file.
    :param csv_path: path to csv file to read broadband readings from.
    :param time_constraints: a tuple storing two datetime objects to indicate what times to return (from, to).
    Set to None to ignore this constraint.
    :param merge_methods: set to True to merge readings from different methods into one line.
    :return: a dict if group_by_method is True, where each key is a method, linked with a list of Reading objects.
    Otherwise, returns a list of Reading objects.
    """
    # Create data structure for storing Reading objects - group by method name if necessary, otherwise use a simple list
    readings = [] if merge_methods else {method: [] for method in constants.RecordingMethod}

    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        row: dict  # Specify row is a dict, to help PyCharm

        # Rather than considering whether to group by method within the for loop, which would be more readable,
        # I have used 2 for loops running similar code, so that the if statement is not re-evaluated repeatedly,
        # which should be slightly faster.
        if merge_methods:
            for row in reader:
                reading = create_reading_from_row(row)
                if check_reading_in_constraints(reading, time_constraints):
                    readings.append(reading)

        else:
            for row in reader:
                reading = create_reading_from_row(row)
                if check_reading_in_constraints(reading, time_constraints):
                    readings[reading.method].append(reading)
            prune_unused_groups(readings)

    # Sort by timestamp, in case the data from csv is out of order
    sort_by_timestamp(readings)

    return readings


# Used by include_reading, implicitly tested by it
def create_reading_from_row(row: dict) -> classes.Reading:
    """ Creates a Reading object from the dict provided - dict must have keys for 'upload', 'download', 'timestamp', and 'method'.
     For use with a method that gets Readings from a file. """
    return classes.Reading(float(row["download"]),
                           float(row["upload"]),
                           classes.Reading.convert_string_to_datetime(row["timestamp"]),
                           constants.RecordingMethod(row["method"]))


# Used by include_reading, implicitly tested by it
def check_reading_in_constraints(reading: classes.Reading, time_constraints: tuple[datetime, datetime] | None):
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
def sort_by_timestamp(readings: dict | list):
    """ For merged, sorts all the readings by timestamp, for unmerged, sorts all the readings within each group by timestamp.
    For use with a method that gets readings from a file. """
    def sort(reading: classes.Reading):
        return reading.timestamp

    if isinstance(readings, list):
        # Sort all readings
        readings.sort(key=sort)
    elif isinstance(readings, dict):
        # Sort within each method
        for method in readings.keys():
            readings[method].sort(key=sort)
