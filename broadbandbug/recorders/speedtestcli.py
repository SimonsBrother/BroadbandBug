from datetime import datetime, timedelta
from time import sleep

import speedtest

from broadbandbug.library.classes import Reading, BaseRecorder
from broadbandbug.library.constants import RecordingMethod, TIMEOUT
from broadbandbug.recorders.common import convert_to_mbs


class SpeedtestCLIRecorder(BaseRecorder):
    def __init__(self, identifier: str = "recorder"):
        super().__init__(identifier)
        self.speedtest_obj = speedtest.Speedtest(secure=True)
        self.speedtest_obj.get_best_server([])

    def process(self):
        # Perform speed test
        self.speedtest_obj.download(threads=1)  # Using None for threads breaks stuff. It works like this.
        if self.stop_event.is_set(): return  # Causes the speedtest to stop where possible, in a controlled way
        self.speedtest_obj.upload(threads=1)

        # Make reading
        results = self.speedtest_obj.results
        reading = Reading(convert_to_mbs(results.download), convert_to_mbs(results.upload), datetime.now(),
                          RecordingMethod.SPEEDTEST_CLI)

        # If the connection dies, wait for some time (otherwise will spam with zeroes)
        if results.download == 0 or results.upload == 0:
            self.get_logger().warning("Connection may be down. Timing out.")
            # Rather than using sleep(30), use while loop that repeatedly compares current time to when the loop started,
            # that breaks when the recorder is told to stop
            t1 = datetime.now()
            while datetime.now() - t1 < timedelta(seconds=TIMEOUT):
                sleep(1)

                # Stop timeout if told to stop
                if self.stop_event.is_set():
                    self.get_logger().info("Interrupting timeout.")
                    break

        return reading
