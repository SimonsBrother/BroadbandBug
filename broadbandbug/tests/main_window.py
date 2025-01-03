import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from broadbandbug.gui.main_window import MainWindow
from broadbandbug.library.classes import BaseRecorder
import broadbandbug.library.constants as constants

constants.RECORDING_DEFAULT_PATH = BaseRecorder.csv_path = Path("./resources/actual.csv")
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
