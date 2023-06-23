from datetime import datetime

import broadbandbug.library.files as files
import broadbandbug.library.constants as consts
from broadbandbug.library.classes import Result

test_csv_path = "test.csv"
test_json_path = "test.json"
files.makeFile(test_csv_path)
files.makeFile(test_json_path)


def test_writeResults():
    files.writeResults(test_csv_path, Result(1, 2, datetime.now().strftime(consts.TIME_FORMAT), consts.METHOD_SPEEDTESTCLI))


def test_readResults():
    print(files.readResults(test_csv_path))


def test_writePalette():
    palettes = {
        consts.METHOD_SPEEDTESTCLI: {"download": "135799", "upload": "123456"},
        "test2": {"download": "a", "upload": "b"}
    }
    files.writePalette(test_json_path, palettes)


def test_readPalette():
    print(files.readPalette(test_json_path))
