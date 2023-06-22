class Results:
    """
    Stores the upload and download speed for easy access
    """
    def __init__(self, download, upload, timestamp, bug_type):
        self.download = download
        self.upload = upload
        self.timestamp = timestamp
        self.bug_type = bug_type

    def __repr__(self):
        return f"Results(download={self.download}, upload={self.upload}," \
               f" timestamp={self.timestamp}, bug_type={self.bug_type})"
