from time import sleep

from broadbandbug.recorders.speedtestcli import SpeedtestCLIRecorder
import threading


# Manual test
def speedtest_cli():
    rec = SpeedtestCLIRecorder("Speedtest CLI test")
    threading.Thread(target=rec.recording_loop).start()
    sleep(120)
    rec.send_stop_signal()

    results = rec.get_new_readings_queue()
    while not results.empty():
        print(results.get())


if __name__ == '__main__':
    speedtest_cli()
