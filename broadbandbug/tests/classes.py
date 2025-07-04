""" Contains all testing functions for the classes module. """
from datetime import datetime

from pytest import raises

from ..library import classes


# Reading instantiation is too simple to test, plus tested in manual tests

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

# logging and BaseRecorder is tested through GUI manual tests
