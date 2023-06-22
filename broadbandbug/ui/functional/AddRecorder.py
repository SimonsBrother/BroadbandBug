from broadbandbug.ui.addrecorder import Ui_AddRecorder

from PyQt6.QtWidgets import QApplication, QDialog


# Adapted from https://www.pythonguis.com/tutorials/pyqt6-creating-dialogs-qt-designer/
class AddRecorder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_AddRecorder()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE


if __name__ == "__main__":
    app = QApplication([])

    dlg = AddRecorder()
    dlg.show()  # Windows are hidden by default

    app.exec()
