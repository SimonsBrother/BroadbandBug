""" Defines most of the classes used throughout BroadbandBug. """
from dataclasses import dataclass
from threading import Event
from queue import Queue
from datetime import datetime
import logging
from typing import ClassVar

from . import constants


@dataclass
class Reading:
    """ Stores the upload and download broadband speed
    :var download: float, the download speed (no specific unit)
    :var upload: float, the upload speed (no specific unit)
    :var timestamp: datetime, when the reading was obtained.
    :var method: RecordingMethod, the method by which this reading was obtained.
    """
    download: float
    upload: float
    timestamp: datetime
    method: constants.RecordingMethod

    # Used for making header in csv file
    attributes: ClassVar[list[str]] = ["download", "upload", "timestamp", "method"]

    def get_timestamp_as_str(self):
        return self.timestamp.strftime(constants.TIME_FORMAT)

    @staticmethod
    # Converts date strings to a datetime
    def convert_string_to_datetime(string: str):
        return datetime.strptime(string, constants.TIME_FORMAT)

    def format_for_csv(self):
        """ Produces a dict in the format needed to save it to a csv file. """
        return {"download": self.download, "upload": self.upload,
                "timestamp": self.get_timestamp_as_str(), "method": self.method.value}


def create_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.setLevel(logging.INFO)

    logger.addHandler(handler)

    return logger


class BaseRecorder:
    # The Queue object used as a buffer for writing to the results file.
    # Multiple recorders may provide data at the same time, so use thread-safe structure like queue.
    # Hidden via underscore because only the BaseRecorder results attribute should be accessed (since modifying the superclass
    # attribute will modify the child class static attributes, but modifying the child attributes will not affect the parent.
    _results_queue = Queue()
    _logger = create_logger()

    def __init__(self, identifier: str):
        """ A base class defining how recorders will run, that is meant to be extended - specifically, recording_loop should be overridden.
        :param identifier: a string identifying the recorder.
        """
        self.identifier = identifier

        self.stop_event = Event()  # This can be set to indicate when the recorder should be stopped.
        self.future = None  # This represents the asynchronous execution of the recording_loop
        BaseRecorder.get_logger().info(f"Created {identifier}")

    # Getters and setters for queue
    @staticmethod
    def get_results_queue() -> Queue:
        """ Gets the results queue. """
        return BaseRecorder._results_queue

    @staticmethod  # Define as static method because regardless of which class it is from, it should only affect BaseRecorder.
    def add_result_to_queue(reading: Reading):
        """ Adds a reading to the queue. """
        BaseRecorder._results_queue.put(reading)

    @staticmethod  # Use this to get the logger, so that only one is used throughout child classes.
    def get_logger() -> logging.Logger:
        """ Returns the BaseRecorder logger. """
        return BaseRecorder._logger

    # This function is to overridden and passed on to the thread executor. It is here as a demonstration only.
    def recording_loop(self):
        """ Repeatedly takes a reading and adds it to the queue. """
        BaseRecorder.get_logger().warning("USING BASE CLASS - FOR TESTING PURPOSES ONLY")
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Get new reading
            now = datetime.now()
            reading = Reading(1, 2, now, constants.RecordingMethod.BT_WEBSITE)

            # Add new Result object to queue
            BaseRecorder.add_result_to_queue(reading)

        # Log that the recorder has stopped.
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has stopped.")

    def start_recording(self, threadpool_executor):
        """ Starts the recorder by submitting the recording function to the threadpool executor passed. """
        # Submit the new BaseRecorder object's recording_loop function to executor, and set the BaseRecorder's future
        self.future = threadpool_executor.submit(self.recording_loop)
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has started.")

    def stop_recording(self):
        BaseRecorder.get_logger().info(f"Stopping '{self.identifier}'...")
        self.stop_event.set()

    def __repr__(self):
        return f"{type(self).__name__} {self.identifier!r} ({'stopped' if self.stop_event.is_set() else 'active'})"
