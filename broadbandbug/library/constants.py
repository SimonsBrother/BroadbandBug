from enum import Enum
from pathlib import Path

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
RECORDING_DEFAULT_PATH = Path("./RECORDING.csv")

class RecordingMethod(Enum):
    SPEEDTEST_CLI = "Speedtest CLI"
    BT_WEBSITE = "BT Website"
    WHICH_WEBSITE = "Which? Website"


LINE_COLORS = {
    RecordingMethod.SPEEDTEST_CLI: ["#0f3071", "#71500f"],
    RecordingMethod.BT_WEBSITE: ["#000000", "#ff0000"],
    RecordingMethod.WHICH_WEBSITE: ["#ce3a38", "#38ccce"],
}


class Browser(Enum):
    CHROME = "Chrome"
    EDGE = "Edge"


METHODS_USING_BROWSER = (RecordingMethod.BT_WEBSITE, RecordingMethod.WHICH_WEBSITE)
TIMEOUT = 30  # How long speedtest cli recorder should wait when the network goes down before trying another test
