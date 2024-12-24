from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton
)

from broadbandbug.library import constants


class RecorderDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recording Method Selector")

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Inline layout for the first combo box
        self.inline_layout = QHBoxLayout()

        # Recording Method Combo Box
        self.recording_label = QLabel("Recording method:")
        self.recording_combo = QComboBox()
        self.recording_combo.addItems([method.value for method in constants.RecordingMethod])
        self.recording_combo.currentIndexChanged.connect(self.toggle_browser_combobox)

        # Add widgets to inline layout
        self.inline_layout.addWidget(self.recording_label)
        self.inline_layout.addWidget(self.recording_combo)

        # Browser layout (Initially hidden)
        self.browser_inline_layout = QHBoxLayout()
        self.browser_label = QLabel("Browser:")
        self.browser_combo = QComboBox()
        self.browser_combo.addItems([browser.value for browser in constants.Browser])
        self.browser_label.setVisible(False)
        self.browser_combo.setVisible(False)
        self.browser_inline_layout.addWidget(self.browser_label)
        self.browser_inline_layout.addWidget(self.browser_combo)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start recording")
        self.cancel_button = QPushButton("Cancel")
        self.start_button.clicked.connect(self.start_recording)
        self.cancel_button.clicked.connect(self.cancel)
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.cancel_button)

        # Add layouts to main layout
        self.main_layout.addLayout(self.inline_layout)
        self.main_layout.addLayout(self.browser_inline_layout)
        self.main_layout.addLayout(self.buttons_layout)

        # Adjust window size dynamically
        self.adjustSize()

    def toggle_browser_combobox(self):
        """Show or hide the Browser combo box based on the selected recording method."""
        is_visible = self.recording_combo.currentText() != constants.RecordingMethod.SPEEDTEST_CLI.value
        self.browser_label.setVisible(is_visible)
        self.browser_combo.setVisible(is_visible)
        self.adjustSize()

    def start_recording(self):
        self.close()

    def cancel(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    dialog = RecorderDialog()
    dialog.show()
    exit(app.exec())
