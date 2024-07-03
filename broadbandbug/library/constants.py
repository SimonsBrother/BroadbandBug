from enum import Enum

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class RecordingMethod(Enum):
    SPEEDTEST_CLI = "Speedtest CLI"
    BT_WEBSITE = "BT Website"
    WHICH_WEBSITE = "Which? Website"


class Browser(Enum):
    CHROME = "Chrome"
    EDGE = "Edge"


METHODS_USING_BROWSER = (RecordingMethod.BT_WEBSITE, RecordingMethod.WHICH_WEBSITE)
TIMEOUT = 30  # How long speedtest cli recorder should wait when the network goes down before trying another test
