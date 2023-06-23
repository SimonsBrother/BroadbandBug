from dataclasses import dataclass


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


@dataclass
class GraphPalette:
    """ Stores the colors for the upload and download speed lines of the graph """
    download: str
    upload: str
