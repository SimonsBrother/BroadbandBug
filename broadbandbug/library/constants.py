from enum import Enum

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class RecordingMethod(Enum):
    SPEEDTEST_CLI = "Speedtest CLI"
    BT_WEBSITE = "BT Website"
    WHICH_WEBSITE = "Which? Website"


class Browser(Enum):
    CHROME = "Chrome"
    EDGE = "Edge"


METHODS_USING_BROWSER = (RecordingMethod.BT_WEBSITE, RecordingMethod.WHICH_WEBSITE)
