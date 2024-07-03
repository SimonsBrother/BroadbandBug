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
        rec.stop_recording()
        try:
            while True:
                i = rec.get_results_queue().get(timeout=5)
                print(i)
        except Empty:
            ...


if __name__ == '__main__':
    speedtest_cli()
