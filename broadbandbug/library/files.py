import csv
from datetime import datetime
from pathlib import Path

import classes
import constants


# TODO: test, make sure this works when compiled
def ensure_file_exists(path: Path | str):
    """ Ensure the file at the path provided exists, creating it if it does not. Returns True if it exists. """
    # Convert from string to path if necessary
    if isinstance(path, str):
        path = Path(path)

    # Try to read from the file specified.
    exists = path.exists()
    # Create file is it doesn't exist
    if not exists:
        if path.is_dir():
            path.mkdir()
        else:
            path.touch()

    return exists


def read_results(csv_path: str, time_constraints: tuple[datetime, datetime] | None, group_by_method: bool) -> dict | list:
    """
    Reads the broadband readings stored in the file at csv_path. May raise any errors from open() statement.
    :param csv_path: path to csv file to read broadband readings from.
    :param time_constraints: a tuple storing two datetime objects to indicate what times to return (from, to). Set to None to ignore this constraint.
    :param group_by_method: set to True to group readings by how they were obtained.
    :return: a dict if group_by_method is True, where each key is a method, linked with a list of Reading objects. Otherwise, returns a list of Reading objects.
    """
    # Create data structure for storing Reading objects - group by method name if necessary, otherwise use a simple list
    readings = {method.value: [] for method in constants.RecordingMethod} if group_by_method else []

    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            row: dict
            result = create_reading_from_row(row)

            # Check if timestamp check is needed, and if the timestamp is in bounds (because time constraints is checked first,
            # lazy eval will prevent the rest of the statement from evaluating and causing an error.
            if time_constraints is None or time_constraints[0] <= result.timestamp <= time_constraints[1]:
                # TODO: minor optimisation: use two separate for loops contained in if statements
                if group_by_method:
                    readings[result.method].append(result)
                else:
                    readings.append(result)

    return readings


def create_reading_from_row(row: dict) -> classes.Reading:
    """ Creates a Reading object from the dict provided - dict must have keys for 'upload', 'download', 'timestamp', and 'method'.
     For use with a method that gets Readings from a file. """
    return classes.Reading(float(row["upload"]),
                           float(row["download"]),
                           classes.Reading.convert_string_to_datetime(row["timestamp"]),
                           constants.RecordingMethod(row["method"]))


def results_writer(csv_path: str, queue, close_event):
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
