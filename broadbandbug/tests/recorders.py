from queue import Empty
from time import sleep

from broadbandbug.recorders.speedtestcli import SpeedtestCLIRecorder
from concurrent.futures import ThreadPoolExecutor


# Manual test
def speedtest_cli():
    with ThreadPoolExecutor(max_workers=2) as threadpool_exe:
        rec = SpeedtestCLIRecorder("Speedtest CLI test")
        rec.start_recording(threadpool_exe)
        sleep(120)
        print("Stopping")
        rec.send_stop_signal()
        results = rec.get_readings_queue()
        while not results.empty():
            print(results.get())


if __name__ == '__main__':
    speedtest_cli()
