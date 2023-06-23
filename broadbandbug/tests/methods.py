from datetime import datetime

import broadbandbug.methods.speedtestcli as speedtestcli
import broadbandbug.library.files as files
import speedtest

test_path = "test.csv"
files.makeFile(test_path)


def test_speedtestcli():
    for i in range(10):
        result = speedtestcli.performSpeedTest(speedtest.Speedtest())
        files.writeResults(test_path, result)
