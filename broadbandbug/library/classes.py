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
    """ TODO document """
    _new_readings_queue: Queue | None = None  # Used to store new readings, which can be used to update graphs. Use
    # thread-safe structure like queue, for interacting with other threads (like a GUI).
    _logger = create_logger()

    def __init__(self, identifier: str = "recorder"):
        """ A base class defining how recorders will run, that is meant to be extended - specifically, recording_loop should be overridden.
        :param identifier: a string identifying the recorder.
        """
        self.identifier = identifier
        self._recorder_running = False

        self.stop_event = Event()  # This can be set to indicate when the recorder should be stopped.
        self.future = None  # This represents the asynchronous execution of the recording_loop function
        BaseRecorder.get_logger().info(f"Created {identifier}")

    # Getters and setters for queue
    @staticmethod
    def get_new_readings_queue() -> Queue:
        """ Gets the readings queue. """
        return BaseRecorder._new_readings_queue

    @staticmethod  # Define as static method because regardless of which class it is from, it should only affect BaseRecorder.
    def add_reading_to_queue(reading: Reading):
        """ Adds a reading to the queue. """
        if BaseRecorder._new_readings_queue is not None:
            BaseRecorder._new_readings_queue.put(reading)

    @staticmethod
    def initialise_new_readings_queue():
        """ Initialises the queue for storing new readings; this is likely to be called before a graph is opened. """
        BaseRecorder._new_readings_queue = Queue()

    @staticmethod
    def stop_new_readings_queue():
        """ Indicates that the queue is not needed; called once the graph are closed """
        BaseRecorder._new_readings_queue = None

    # Get logger
    @staticmethod  # Use this to get the logger, so that only one is used throughout child classes.
    def get_logger() -> logging.Logger:
        """ Returns the BaseRecorder logger. """
        return BaseRecorder._logger

    # Get whether the recorder is running
    @property
    def recorder_running(self) -> bool:
        return self._recorder_running

    def recording_loop(self):
        """ Repeatedly takes a reading and adds it to the queue. """
        self.prepare()
        self.set_recorder_running()
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            reading = self.process()

            # Add new Reading object to queue
            BaseRecorder.add_reading_to_queue(reading)

        self.cleanup()
        self.set_recorder_stopped()

    def prepare(self):
        """ Function called before the recording loop starts. For overriding. """
        pass

    def process(self) -> Reading:
        """ This function is to be overridden. It is here for demonstration purposes only. """
        BaseRecorder.get_logger().warning("USING BASE CLASS, WHICH IS FOR TESTING PURPOSES ONLY")
        return Reading(1, 2, datetime.now(), constants.RecordingMethod.BSC)

    def cleanup(self):
        """ Function called after the recording loop ends. For overriding. """
        pass

    def set_recorder_running(self):
        """ Indicates that the recorder has started. """
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has started.")
        self._recorder_running = True

    def send_stop_signal(self):
        """ Sends a signal to the recorder to stop. The recorder may not stop immediately. """
        BaseRecorder.get_logger().info(f"Stopping '{self.identifier}'...")
        self.stop_event.set()

    def set_recorder_stopped(self):
        """ Indicates that the recorder has stopped. """
        # Log that the recorder has stopped.
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has stopped.")
        self._recorder_running = False

    def __repr__(self):
        return f"{type(self).__name__}: {self.identifier!r} ({'stopped' if self.recorder_running else 'active'})"
