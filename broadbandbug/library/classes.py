from dataclasses import dataclass


class Result:
    """ Stores the upload and download speed for easy access """
    def __init__(self, download, upload, timestamp, bug_type):
        self.download = download
        self.upload = upload
        self.timestamp = timestamp
        self.bug_type = bug_type

    def __repr__(self):
        return f"Result(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, bug_type={self.bug_type})"


@dataclass
class GraphPalette:
    """ Stores the colors for the upload and download speed lines of the graph """
    download: str
    upload: str
