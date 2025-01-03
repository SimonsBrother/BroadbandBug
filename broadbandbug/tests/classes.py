""" Contains all testing functions for the classes module. """
# TODO
from datetime import datetime
from time import sleep
import concurrent.futures as futures

from pytest import raises

from ..library import classes


# Reading instantiation is too simple to test

# Test convert_string_to_datetime (abbreviated to cstdt) works as expected
def test_valid_cstdt():
    assert classes.Reading.convert_string_to_datetime("10/12/2013 05:57:30") == datetime(2013, 12, 10, 5, 57, 30)
    assert classes.Reading.convert_string_to_datetime("1/1/0001 0:0:0") == datetime(1, 1, 1, 0, 0, 0)


# Test convert_string_to_datetime (abbreviated to cstdt) fails where expected (combined under one function for simplicity)
def test_invalid_cstdt():
    # Blank string
    with raises(ValueError):
        classes.Reading.convert_string_to_datetime("")

    # Invalid format, wrong character
    with raises(ValueError):
        classes.Reading.convert_string_to_datetime("10:12/2013 05:57:30")

    # Invalid format, missing space
    with raises(ValueError):
        classes.Reading.convert_string_to_datetime("10:12/201305:57:30")

    # Invalid month
    with raises(ValueError):
        classes.Reading.convert_string_to_datetime("10/13/2013 05:57:30")

    # Invalid seconds
    with raises(ValueError):
        classes.Reading.convert_string_to_datetime("10/12/2013 05:57:60")


# create_logger is implicitly tested by BaseRecorder tests


# Test BaseRecorder can be instantiated, added to threadpool, stopped, and can queue Readings.
def test_base_recorder():
    # Test successful instantiation
    base_rec = classes.BaseRecorder("Test BaseRecorder")

    # Test repr
    print(f"\n{base_rec}")

    # Test logger can be accessed
    base_rec.get_logger().critical("Test log access - successful if you can see this")

    # Test recording
    assert classes.BaseRecorder.get_results_queue().qsize() == 0
    with futures.ThreadPoolExecutor(2) as exe:
        base_rec.indicate_recorder_started(exe)
        sleep(0.2)
        base_rec.send_stop_signal()

    # Check successfully added Readings to queue
    assert classes.BaseRecorder.get_results_queue().qsize() > 0
    assert isinstance(base_rec.get_results_queue().get(), classes.Reading)

    # Check repr shows stopped
    print(f"{base_rec}")
