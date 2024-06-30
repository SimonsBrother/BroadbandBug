""" Defines classes used throughout BroadbandBug. """

from threading import Event

from selenium.webdriver.remote.webdriver import WebDriver


class Result:
    def __init__(self, download, upload, timestamp: str, method: str):
        # TODO: double check documentation here
        """
        Stores the upload and download speed for easy access
        :param download: value for download speed
        :param upload: value for upload speed
        :param timestamp: a string that represents the time and date the result was obtained
        :param method: the method used to obtain the result
        """
        self.download = float(download)
        self.upload = float(upload)
        self.timestamp = timestamp
        self.method = method

    def __repr__(self):
        return f"Result(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, method={self.method})"


# TODO: Add type hints and switch to snake case
class Recorder:
    def __init__(self, identifier: str, take_reading_function, args: tuple, results_queue):
        """
        :param identifier: a string identifying the recorder.
        :param take_reading_function: the function to be called to take a reading of bandwidth (possibly opening a webpage).
        :param args: the arguments needed to run the reading function.
        :param results_queue: the Queue object used to write to the results csv file - this is passed in because multiple recorders may use the same queue.
        """
        self.identifier = identifier
        self.method_function = take_reading_function
        self.args = args  # TODO replace with kwargs
        self.results_queue = results_queue

        self.stop_event = Event()  # This can set or unset to indicate when the recorder should be stopped.
        self.future = None  # TODO: Document

    # This function is to be passed on to the thread executor
    # TODO: change name to verb
    def recording(self):
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Add new Result object to queue
            self.results_queue.put(self.method_function(*self.args))

        # Go through the arguments passed, and check for any WebDriver objects, and close them
        # TODO: have a custom shutdown function (maybe make recording methods OOP)
        for arg in self.args:
            if isinstance(arg, WebDriver):
                arg.quit()

        print(f"{self.identifier} has stopped.")

    # TODO: what is tp executor
    def startRecording(self, tp_executor):
        # Submit the new Recorder object's startRecording function to executor, and set the Recorder's future
        self.future = tp_executor.submit(self.recording)
        print(f"{self.identifier} has started.")

    def stopRecording(self):
        print(f"Stopping {self.identifier}...")  # TODO: Switch to logging
        self.stop_event.set()

    # TODO: check this
    def __repr__(self):
        return f"Recorder({self.identifier}, {self.method_function}, {self.future})"
