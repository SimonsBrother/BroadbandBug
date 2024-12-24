import sys
from queue import Queue

from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QPushButton, QDateTimeEdit, QCheckBox,
                             QLabel, QFormLayout, QHBoxLayout)
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtGui import QFont

import broadbandbug.library.files as files
import broadbandbug.library.constants as constants
from broadbandbug.gui.graph_windows import MergedGraphWindow, UnmergedGraphWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recording and Graphing Application")
        self.graph = None

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
        self.start_button = QPushButton("Start recording")
        self.start_button.clicked.connect(self.on_start_recording)

        # Pause Recording Button
        self.pause_button = QPushButton("Pause recording")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.on_pause_recording)

        # Make buttons the same width (use the wider of the two)
        button_width = max(self.start_button.sizeHint().width(),
                           self.pause_button.sizeHint().width())
        self.start_button.setFixedWidth(button_width)
        self.pause_button.setFixedWidth(button_width)

        # Add buttons vertically and centered
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)

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

    def on_start_recording(self):
        # Disable start button and enable pause button
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)

    def on_pause_recording(self):
        # Disable pause button and enable start button
        self.pause_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def update_times(self):
        checked = self.limit_by_time_checkbox.isChecked()
        self.start_datetime.setEnabled(checked)
        self.end_datetime.setEnabled(checked)

    def show_graph(self):
        merge_methods = self.merge_method_checkbox.isChecked()
        if self.limit_by_time_checkbox.isChecked():
            time_constraints = (self.start_datetime.dateTime().toPyDateTime(), self.end_datetime.dateTime().toPyDateTime())
        else:
            time_constraints = None

        readings = files.read_results(constants.RECORDING_DEFAULT_PATH, time_constraints, merge_methods)

        queue = Queue()

        if merge_methods:
            self.graph = MergedGraphWindow(readings, queue, time_constraints)
        else:
            self.graph = UnmergedGraphWindow(readings, queue, time_constraints)

        self.graph.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()