from datetime import datetime, timedelta
from time import sleep

import speedtest

from broadbandbug.library.classes import Reading, BaseRecorder
from broadbandbug.library.constants import RecordingMethod, TIMEOUT
from broadbandbug.methods.common import convertToMbs


# TODO test
class SpeedtestCLIRecorder(BaseRecorder):
    def __init__(self, identifier: str, num_threads=None | int):
        super().__init__(identifier)
        self.num_threads = num_threads
        self.speedtest_obj = speedtest.Speedtest()
        self.speedtest_obj.get_best_server([])

    def recording_loop(self):
        # Repeat until the recorder is stopped
        while not self.stop_event.is_set():
            # Perform speed test
            self.speedtest_obj.download(threads=self.num_threads)
            if self.stop_event.is_set(): break
            self.speedtest_obj.upload(threads=self.num_threads)

            # Make reading
            results = self.speedtest_obj.results
            timestamp = datetime.now()
            reading = Reading(convertToMbs(results.download), convertToMbs(results.upload), timestamp,
                              RecordingMethod.SPEEDTEST_CLI)

            # Add new Result object to queue
            BaseRecorder.add_result_to_queue(reading)

            # If the connection dies, wait for 30 seconds (otherwise will spam with zeroes)
            if results.download == 0 or results.upload == 0:
                # Rather than using sleep(30), use while loop that repeatedly compares current time to when the loop started,
                # that breaks when the recorder is told to stop
                t1 = datetime.now()
                while datetime.now() - t1 < timedelta(seconds=30):
                    sleep(1)

                    # Stop timeout if told to stop
                    if self.stop_event.is_set():
                        break

        # Log that the recorder has stopped.
        BaseRecorder.get_logger().info(f"Recorder '{self.identifier}' has stopped.")
