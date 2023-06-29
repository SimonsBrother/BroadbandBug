from threading import Event

from selenium.webdriver.remote.webdriver import WebDriver


class Result:
    def __init__(self, download, upload, timestamp: str, method: str):
        """
        Stores the upload and download speed for easy access
        :param download: value for download speed; converted to float
        :param upload: value for upload speed; converted to float
        :param timestamp: a string that represents the time and date the result was obtained
        :param method: the method used to obtain the result (a constant)
        """
        self.download = float(download)
        self.upload = float(upload)
        self.timestamp = timestamp
        self.method = method

    def __repr__(self):
        return f"Result(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, method={self.method})"


class Recorder:
    def __init__(self, identifier: str, method_function, args: tuple, results_queue):
        """
        :param identifier: a string identifying the recorder
        :param method_function: the function to be called to take a reading of bandwidth
        :param args: the arguments needed to operate the method function
        :param results_queue: the Queue object used to write to the results csv file
        """
        self.identifier = identifier
        self.method_function = method_function
        self.args = args
        self.results_queue = results_queue
        self.stop_event = Event()
        self.future = None

    # This function is to be passed on to the thread executor
    def recording(self):
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Add new Result object to queue
            self.results_queue.put(self.method_function(*self.args))

        # Go through the arguments passed, and check for any WebDriver objects, and close them
        for arg in self.args:
            if isinstance(arg, WebDriver):
                arg.quit()

        print(f"{self.identifier} has stopped.")

    def startRecording(self, tp_executor):
        # Submit the new Recorder object's startRecording function to executor, and set the Recorder's future
        self.future = tp_executor.submit(self.recording)
        print(f"{self.identifier} has started.")

    def stopRecording(self):
        print(f"Stopping {self.identifier}...")
        self.stop_event.set()

    def __repr__(self):
        return f"Recorder({self.identifier}, {self.method_function}, {self.future})"
