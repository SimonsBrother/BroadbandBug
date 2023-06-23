from datetime import datetime

from broadbandbug.library.classes import Result
from broadbandbug.library.constants import TIME_FORMAT, METHOD_SPEEDTESTCLI

import speedtest


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

    speedtest_obj.get_best_server()
    speedtest_obj.download(threads=num_threads)
    speedtest_obj.upload(threads=num_threads)

    timestamp = datetime.now().strftime(TIME_FORMAT)

    return Result(convertToMbs(speedtest_obj.results.download), convertToMbs(speedtest_obj.results.upload), timestamp,
                  METHOD_SPEEDTESTCLI)


if __name__ == "__main__":
    spdtest = speedtest.Speedtest()

    print(performSpeedTest(spdtest))
