from datetime import datetime

import broadbandbug.library.files as files
import broadbandbug.library.constants as consts
from broadbandbug.library.classes import Result

test_path = "test.csv"
files.makeFile(test_path)


def test_writeResults():
    files.writeResults(test_path, Result(1, 2, datetime.now().strftime(consts.TIME_FORMAT), consts.METHOD_SPEEDTESTCLI))


def test_readResults():
    print(files.readResults(test_path))
