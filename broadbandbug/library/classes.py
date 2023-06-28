from threading import Event


class Result:
    """ Stores the upload and download speed for easy access """

    def __init__(self, download, upload, timestamp: str, method):
        self.download = float(download)
        self.upload = float(upload)
        self.timestamp = timestamp
        self.method = method

    def __repr__(self):
        return f"Result(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, bug_type={self.method})"


class Recorder:
    def __init__(self, identifier: str, method_function, params: tuple, results_queue):
        """
        :param identifier: a string identifying the recorder
        :param method_function: the function to be called to take a reading of bandwidth
        :param params: the parameters needed to operate the method function
        :param results_queue: the Queue object used to write to the results csv file
        """
        self.identifier = identifier
        self.method_function = method_function
        self.parameters = params
        self.results_queue = results_queue
        self.stop_event = Event()
        self.future = None

    # This function is to be passed on to the thread executor
    def recording(self):
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Add new Result object to queue
            self.results_queue.put(self.method_function(*self.parameters))

        # Signify the recording has stopped
        return True

    def startRecording(self, tp_executor):
        # Submit the new Recorder object's startRecording function to executor, and set the Recorder's future
        self.future = tp_executor.submit(self.recording)

    def stopRecording(self):
        self.stop_event.set()

    def __repr__(self):
        return f"Recorder({self.identifier}, {self.method_function}, {self.future})"
