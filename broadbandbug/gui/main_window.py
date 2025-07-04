from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QPushButton, QDateTimeEdit, QCheckBox,
                             QLabel, QFormLayout, QDialog, QMessageBox)
from PyQt6.QtCore import QDateTime, Qt, QObject, pyqtSignal, QThread
from PyQt6.QtGui import QFont

import broadbandbug.library.classes as classes
import broadbandbug.library.files as files
import broadbandbug.library.constants as constants
from broadbandbug.gui.closing_window import ClosingDialog
from broadbandbug.gui.graph_windows import MergedGraphWindow, UnmergedGraphWindow
from broadbandbug.gui.recorder_selection import RecorderDialog
from broadbandbug.recorders import speedtestcli, which_website


class RecorderWorker(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, recorder_type: type[classes.BaseRecorder], **kwargs):
        super().__init__()
        self.recorder_type = recorder_type
        self.kwargs = kwargs
        self.recorder = None

    def run(self):
        self.recorder = self.recorder_type(**self.kwargs)
        self.started.emit()
        try:
            self.recorder.recording_loop()
        except FileNotFoundError:
            # The file should automatically be created when the application starts.
            # This should never happen unless the user deletes the file after the application starts.
            self.error.emit("No output file: No recording file was found, please restart the application.")
        except PermissionError:
            self.error.emit("Permission denied: Permission denied, please ensure you have full access to the recording file, or run the application as an administrator.")
        except Exception as e:
            self.error.emit(f"Unexpected error: "
                            f"An unknown error occurred, please restart the application.\n\nDetails:\n{e}")
        self.stopped.emit()

    def send_stop_signal(self):
        if self.recorder is not None:
            self.recorder.send_stop_signal()
        # It is possible for recorder to be None if the user closes the window immediately after starting a recorder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recording and Graphing Application")
        self.graph_dlg = self.recorder_dlg = self.recorder_worker = self.thread = None

        # Create a much larger font
        app_font = QFont()
        app_font.setPointSize(18)  # Substantially increased font size
        QApplication.setFont(app_font)

        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create Recording Tab
        self.recording_tab = QWidget()
        self.recording_layout = QVBoxLayout()

        # Vertical layout for buttons (centered)
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Start Recording Button
        self.start_button_default_text = "Start recording"
        self.start_button = QPushButton(self.start_button_default_text)
        self.start_button.clicked.connect(self.on_start_recording_pressed)

        # Pause Recording Button
        self.stop_button_default_text = "Stop recording"
        self.stop_button = QPushButton(self.stop_button_default_text)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.on_stop_recording_pressed)

        # Make buttons the same width (use the wider of the two)
        button_width = max(self.start_button.sizeHint().width(),
                           self.stop_button.sizeHint().width())
        self.start_button.setFixedWidth(button_width)
        self.stop_button.setFixedWidth(button_width)

        # Add buttons vertically and centered
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Add centered button layout to main layout
        self.recording_layout.addLayout(button_layout)

        self.recording_tab.setLayout(self.recording_layout)
        self.tab_widget.addTab(self.recording_tab, "Recording")

        # Create Graph Tab
        self.graph_tab = QWidget()
        self.graph_layout = QFormLayout()

        limit_by_time_box = QVBoxLayout()
        # Set Current Time Button
        self.limit_by_time_checkbox = QCheckBox("Limit by time")
        self.limit_by_time_checkbox.setFixedSize(self.limit_by_time_checkbox.sizeHint())
        self.limit_by_time_checkbox.setChecked(True)
        self.limit_by_time_checkbox.stateChanged.connect(self.update_times)
        # Center the checkbox
        limit_by_time_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        limit_by_time_box.addWidget(self.limit_by_time_checkbox)

        self.graph_layout.addRow(limit_by_time_box)

        # Start DateTime Edit
        self.start_datetime_label = QLabel("Start date and time:")
        self.start_datetime = QDateTimeEdit()
        self.start_datetime.setCalendarPopup(True)
        # Set to current datetime by default
        self.start_datetime.setDateTime(QDateTime.currentDateTime())
        self.start_datetime.setFixedSize(self.start_datetime.sizeHint())
        self.graph_layout.addRow(self.start_datetime_label, self.start_datetime)
        # End DateTime Edit
        self.end_datetime_label = QLabel("End date and time:")
        self.end_datetime = QDateTimeEdit()
        self.end_datetime.setCalendarPopup(True)
        # Set to current datetime by default
        self.end_datetime.setDateTime(QDateTime.currentDateTime())
        self.end_datetime.setFixedSize(self.end_datetime.sizeHint())
        self.graph_layout.addRow(self.end_datetime_label, self.end_datetime)

        # Merge Method Checkbox
        self.merge_method_checkbox = QCheckBox("Merge method readings")
        self.merge_method_checkbox.setFixedSize(self.merge_method_checkbox.sizeHint())

        # Plot Graph Button
        self.plot_graph_button = QPushButton("Plot graph")
        self.plot_graph_button.setFixedSize(self.plot_graph_button.sizeHint())
        self.plot_graph_button.clicked.connect(self.show_graph)

        # Add layouts and widgets to graph layout
        self.graph_layout.addRow(self.merge_method_checkbox)
        self.graph_layout.addRow(self.plot_graph_button)

        self.graph_tab.setLayout(self.graph_layout)
        self.tab_widget.addTab(self.graph_tab, "Graph")

        # Adjust window size to fit contents
        self.adjustSize()

    def on_start_recording_pressed(self):
        # Show recording selection dialog
        if not self.recorder_dlg:
            self.recorder_dlg = RecorderDialog()
        response = self.recorder_dlg.exec()

        # If cancel clicked, return
        if response == QDialog.DialogCode.Rejected:
            return

        self.start_button.setEnabled(False)
        self.start_button.setText("Starting...")

        # Get data from dialog
        method = constants.RecordingMethod(self.recorder_dlg.recording_combo.currentText())
        browser = constants.Browser(self.recorder_dlg.browser_combo.currentText())

        # Get required recorder with match case
        match method:
            case constants.RecordingMethod.SPEEDTEST_CLI:
                recorder = speedtestcli.SpeedtestCLIRecorder
            case _:
                recorder = None

        # Make the wrapper and pass it to a new thread
        self.thread = QThread()
        self.recorder_worker = RecorderWorker(recorder)
        self.recorder_worker.moveToThread(self.thread)

        self.thread.started.connect(self.recorder_worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.recorder_worker.started.connect(self.on_recorder_started)
        self.recorder_worker.stopped.connect(self.on_recorder_stopped)
        self.recorder_worker.stopped.connect(self.thread.quit)
        self.recorder_worker.stopped.connect(self.recorder_worker.deleteLater)
        self.recorder_worker.error.connect(self.on_error_received)

        self.thread.start()

    def on_recorder_started(self):
        # Disable start button and enable pause button
        self.stop_button.setEnabled(True)
        self.start_button.setText("Started")

    def on_stop_recording_pressed(self):
        self.stop_button.setEnabled(False)
        self.stop_button.setText("Stopping...")
        # Send stop signal
        self.recorder_worker.send_stop_signal()

    def on_recorder_stopped(self):
        self.start_button.setEnabled(True)
        self.start_button.setText(self.start_button_default_text)
        self.stop_button.setText(self.stop_button_default_text)

    def update_times(self):
        checked = self.limit_by_time_checkbox.isChecked()
        self.start_datetime.setEnabled(checked)
        self.end_datetime.setEnabled(checked)

    def show_graph(self):
        # TODO error handling
        merge_methods = self.merge_method_checkbox.isChecked()
        if self.limit_by_time_checkbox.isChecked():
            time_constraints = (self.start_datetime.dateTime().toPyDateTime(), self.end_datetime.dateTime().toPyDateTime())
        else:
            time_constraints = None

        readings = files.read_results(constants.RECORDING_DEFAULT_PATH, time_constraints, merge_methods)

        if merge_methods:
            self.graph_dlg = MergedGraphWindow(readings, time_constraints)
        else:
            self.graph_dlg = UnmergedGraphWindow(readings, time_constraints)

        self.graph_dlg.show()

    def closeEvent(self, event):
        """ Ensures everything is closed as intended, particularly the recorder and its thread. """
        if self.recorder_worker and self.recorder_worker.recorder.recorder_running:
            self.on_stop_recording_pressed() # Re-use
            self.setDisabled(True)
            ClosingDialog(self).exec()

            # Attempt to quit thread (this has to be done or else it waits forever), may fail if it was already deleted.
            try:
                self.thread.quit()
            except RuntimeError:
                pass
            self.thread.wait()

        event.accept()

    def on_error_received(self, msg: str):
        QMessageBox.critical(self, *msg.split(": "))


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()