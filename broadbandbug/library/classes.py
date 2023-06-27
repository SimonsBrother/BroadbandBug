from threading import Event


class Result:
    """ Stores the upload and download speed for easy access """

    def __init__(self, download, upload, timestamp, method):
        self.download = float(download)
        self.upload = float(upload)
        self.timestamp = timestamp
        self.method = method

    def __repr__(self):
        return f"Result(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, bug_type={self.method})"


class Recorder:
    def __init__(self, identifier: str, method_function, params: tuple):
        """
        :param recorders: the dictionary used to store active recorders (with identifiers as keys to each Recorder object)
        :param identifier: a string identifying the recorder
        :param method_function: the function to be called to take a reading of bandwidth
        :param params: the parameters needed to operate the method function
        """
        self.identifier = identifier
        self.method_function = method_function
        self.parameters = params
        self.stop_event = Event()
        self.future = None

    def recording(self):
        # This function is to be passed on to the thread executor
        while not self.stop_event.is_set():
            # todo store return values in queue; add queue attribute
            self.method_function(*self.parameters)

        # Signify the recording has stopped
        return True

    def startRecording(self, tp_executor):
        # Submit the new Recorder object's startRecording function to executor, and set the Recorder's future
        self.future = tp_executor.submit(self.recording)

    def stopRecording(self):
        self.stop_event.set()

    def __repr__(self):
        return f"Recorder({self.identifier}, {self.method_function}, {self.future})"
