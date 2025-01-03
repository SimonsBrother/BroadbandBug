""" Defines most of the classes used throughout BroadbandBug: Reading, BaseRecorder. See individual documentation. """
from dataclasses import dataclass
from threading import Event
from queue import Queue
from datetime import datetime
import logging
from typing import ClassVar
import csv

from . import constants


@dataclass
class Reading:
    """ Represents a single reading of the broadband speed at some point in time.
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
    """ A base class defining how recorders will run, that is meant to be extended.
    The methods 'prepare', 'process', and 'cleanup' are meant to be overridden.
    The recording_loop is meant to be passed to a thread
    """
    _new_readings_queue: Queue | None = None  # Used to store new readings, which can be used to update graphs. Use
    # thread-safe structure like queue, for interacting with other threads (like a GUI).
    _logger = create_logger()
    csv_path = constants.RECORDING_DEFAULT_PATH

    def __init__(self, identifier: str = "recorder"):
        """ A base class defining how recorders will run, that is meant to be extended.
        :param identifier: a string identifying the recorder.
        """
        self.identifier = identifier
        self._recorder_running = False

        self.stop_event = Event()  # This can be set to indicate when the recorder should be stopped.
        BaseRecorder.get_logger().info(f"Created {identifier}")

    # New readings queue related functions
    @staticmethod
    def get_new_readings_queue() -> Queue:
        """ Gets the readings queue. """
        return BaseRecorder._new_readings_queue

    @staticmethod  # Static method because regardless of which class it is from, it should only affect BaseRecorder.
    def add_reading_to_queue(reading: Reading):
        """ Adds a reading to the queue. """
        BaseRecorder._new_readings_queue.put(reading)

    @staticmethod
    def initialise_new_readings_queue():
        """ Initialises the queue for storing new readings; this is likely to be called before a graph is opened. """
        BaseRecorder._new_readings_queue = Queue()

    @staticmethod
    def delete_new_readings_queue():
        """ Indicates that the queue is not needed; likely to be called once a graph is closed. """
        # This implicitly deletes the queue, saving memory
        BaseRecorder._new_readings_queue = None
    # End of new readings queue related functions

    # Get logger
    @staticmethod  # Use this to get the logger, so that only one is used throughout child classes.
    def get_logger() -> logging.Logger:
        """ Returns the BaseRecorder logger. """
        return BaseRecorder._logger

    def recording_loop(self):
        """ Opens the CSV file, repeatedly takes a reading, adds it to the new readings queue and CSV file.
        May raise any errors from open() statement. """
        # Open CSV file and initialise writer
        with open(BaseRecorder.csv_path, "a+") as csv_file:
            writer = csv.DictWriter(csv_file, Reading.attributes)

            # Create header if it does not yet exist
            if csv_file.readline() != "":
                writer.writeheader()
            csv_file.seek(0)

            self.prepare()
            self.indicate_recorder_started()
            # Repeat until the recorder is stopped
            while not self.stop_event.is_set():
                reading = self.process()

                # Attempt to add new Reading object to queue
                if BaseRecorder._new_readings_queue is not None:
                    BaseRecorder.add_reading_to_queue(reading)

                # Record to file
                writer.writerow(reading.format_for_csv())
                csv_file.flush()  # Flush buffer to ensure there is no data to be written

        self.cleanup()
        self.indicate_recorder_stopped()

    # Functions to override
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
    # End of functions to override

    # Recorder running state functions
    def indicate_recorder_started(self):
        """ Indicates that the recorder has started. For use within the recording_loop, shouldn't be used elsewhere. """
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has started.")
        self._recorder_running = True

    def send_stop_signal(self):
        """ Sends a signal to the recorder to stop. The recorder may not stop immediately. """
        BaseRecorder.get_logger().info(f"Stopping '{self.identifier}'...")
        self.stop_event.set()

    def indicate_recorder_stopped(self):
        """ Indicates that the recorder has stopped. For use within the recording_loop, shouldn't be used elsewhere. """
        # Log that the recorder has stopped.
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has stopped.")
        self._recorder_running = False

    @property
    def recorder_running(self) -> bool:
        return self._recorder_running
    # End of recorder running state functions

    def __repr__(self):
        return f"{type(self).__name__}: {self.identifier!r} ({'stopped' if self.recorder_running else 'active'})"
