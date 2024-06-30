""" Defines most of the classes used throughout BroadbandBug. """
from dataclasses import dataclass
from threading import Event
from queue import Queue
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver


@dataclass
class BroadbandReading:
    """ Stores the upload and download broadband speed
    :var download: test (no specific unit)
    :var upload: the upload speed (no specific unit)
    :var timestamp: when the reading was obtained.
    :var method: the method by which this reading was obtained.
    """
    download: float
    upload: float
    timestamp: str  # TODO: replace with datetime or actual timestamp (seconds since epoch)?
    method: str  # TODO: replace once constants are replaced


class Recorder:
    # The Queue object used as a buffer that for writing to the results file.
    # A queue is used because it is thread safe, which is important since multiple recorders may provide data at the same time.
    results_queue = Queue()

    def __init__(self, identifier: str, take_reading_function, args: tuple):
        """
        :param identifier: a string identifying the recorder.
        :param take_reading_function: the function to be called to take a reading of bandwidth (possibly opening a webpage).
        :param args: the arguments needed to run the reading function.

        """
        self.identifier = identifier
        self.take_reading_function = take_reading_function
        self.args = args  # TODO remove when replacing recording method

        self.stop_event = Event()  # This can set to indicate when the recorder should be stopped.
        self.future = None  # This represents the asynchronous execution of the recording_loop

    # This function is to be passed on to the thread executor.
    def recording_loop(self):
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Add new Result object to queue
            Recorder.results_queue.put(self.take_reading_function(*self.args))

        # Go through the arguments passed, and check for any WebDriver objects, and close them
        # TODO: have a custom shutdown function (maybe make recording methods OOP)
        for arg in self.args:
            if isinstance(arg, WebDriver):
                arg.quit()

        print(f"{self.identifier} has stopped.")

    @classmethod  # Define as class method because it affects class state
    def add_result_to_queue(cls, reading: BroadbandReading):
        """ Adds some reading to the queue. """
        Recorder.results_queue.put(reading)

    def start_recording(self, threadpool_executor):
        # Submit the new Recorder object's recording_loop function to executor, and set the Recorder's future
        self.future = threadpool_executor.submit(self.recording_loop)
        print(f"{self.identifier} has started.")

    def stop_recording(self):
        print(f"Stopping {self.identifier}...")  # TODO: Switch to logging
        self.stop_event.set()

    # TODO: test chatgpt's repr
    def __repr__(self):
        return (f"Recorder(identifier={self.identifier!r}, "
                f"take_reading_function={self.take_reading_function.__name__}, "
                f"args={self.args!r}, "
                f"stop_event_set={self.stop_event.is_set()})")
