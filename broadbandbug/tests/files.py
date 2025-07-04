from pathlib import Path
from threading import Thread
from time import sleep

from ..library import classes
from ..library import files


test_path = Path("./broadbandbug/tests/resources").absolute()


# Test ensure_file_exists (abbreviated to efe)
def test_efe_file_exists():
    print(test_path / "existing_file.txt")
    # Test already existing files are recognised as such
    existing_file = test_path / "existing_file.txt"
    assert files.ensure_file_exists(existing_file, False)


def test_efe_dir_exists():
    # Test already existing directories are recognised as such
    existing_dir = test_path / "existing_dir"
    assert files.ensure_file_exists(existing_dir, True)


def test_efe_file_doesnt_exist():
    # Test non-existing files are created
    non_existing_file = test_path / "non_existing_file.txt"
    try:
        assert not non_existing_file.exists()  # Ensure it doesn't exist
        assert not files.ensure_file_exists(non_existing_file, False)  # Ensure function recognised it didn't exist
        assert non_existing_file.exists()  # Ensure it now exists

    except AssertionError as e:
        raise e  # Re-raise error, doing it this way allows the "finally" clause to delete file if needed.
    finally:
        try:
            non_existing_file.unlink()  # Delete for future tests
        except:
            print("Could not delete file.")


def test_efe_dir_doesnt_exist():
    # Test non-existing directories are created
    non_existing_dir = test_path / "non_existing_dir"
    try:
        assert not non_existing_dir.exists()
        assert not files.ensure_file_exists(non_existing_dir, True)
        assert non_existing_dir.exists()

    except AssertionError as e:
        raise e
    finally:
        try:
            non_existing_dir.rmdir()
        except:
            print("Could not delete dir.")


# read_results is tested by plotting tests, which is tested manually.


# Manual test - expect results_writer_test_file.csv to have stuff in resources dir
def test_results_writer():
    results_writer_test_file = test_path / "results_writer_test_file.csv"
    classes.BaseRecorder.csv_path = results_writer_test_file
    files.ensure_file_exists(results_writer_test_file, False)

    base_rec = classes.BaseRecorder("Results writer testing")

    # Start recording
    thread = Thread(target=base_rec.recording_loop)
    thread.start()
    sleep(0.01)

    # Stop everything
    base_rec.send_stop_signal()
