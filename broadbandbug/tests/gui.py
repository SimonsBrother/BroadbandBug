import sys

from PyQt6.QtWidgets import QApplication
from matplotlib import pyplot

from broadbandbug.gui.main_window import MainWindow
import broadbandbug.library.constants as constants

constants.RECORDING_DEFAULT_PATH = "resources/actual.csv"
app = QApplication(sys.argv)
window = MainWindow(pyplot)
window.show()
sys.exit(app.exec())
