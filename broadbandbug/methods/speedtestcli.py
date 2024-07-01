from datetime import datetime
from time import sleep

from broadbandbug.library.classes import Reading
from broadbandbug.library.constants import TIME_FORMAT, RecordingMethod
METHOD_SPEEDTESTCLI = RecordingMethod.SPEEDTEST_CLI

import speedtest

"""
When instantiating speedtest object, do:
speedtest_obj = speedtest
speedtest_obj.get_best_server()
"""


# Converts from bits/s to megabits/s.
def convertToMbs(bps):
    return float(bps) / 1_000_000


def performSpeedTest(speedtest_obj, num_threads=None):
    """
    Performs a speedtest with the speedtest-cli library using the Speedtest object and number of threads specified.
    Performs a download test, then an upload test.

    :param speedtest_obj: a Speedtest object
    :param num_threads: the number of threads
    :return: a Result object
    """

    speedtest_obj.download(threads=num_threads)
    speedtest_obj.upload(threads=num_threads)

    timestamp = datetime.now().strftime(TIME_FORMAT)

    # If the connection dies, wait for 30 seconds (otherwise will spam with zeroes)
    if speedtest_obj.results.download == 0 or speedtest_obj.results.upload == 0:
        sleep(30)

    return Reading(convertToMbs(speedtest_obj.results.download), convertToMbs(speedtest_obj.results.upload), timestamp,
                   METHOD_SPEEDTESTCLI)


if __name__ == "__main__":
    spdtest = speedtest.Speedtest()
    spdtest.get_best_server()
    while True:
        print(performSpeedTest(spdtest))
