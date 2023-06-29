from broadbandbug.ui.addrecorder import Ui_AddRecorder
from broadbandbug.library.constants import SUPPORTED_METHODS, SUPPORTED_BROWSERS, METHODS_USING_BROWSERS

from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox


# Adapted from https://www.pythonguis.com/tutorials/pyqt6-creating-dialogs-qt-designer/
class AddRecorder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_AddRecorder()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE
        self.ui.methodComboBox.addItems(SUPPORTED_METHODS)
        self.ui.driverComboBox.addItems(SUPPORTED_BROWSERS)

        self.ui.buttonBox.accepted.connect(self.okClicked)
        self.ui.methodComboBox.currentIndexChanged.connect(self.methodChanged)

        # Call to ensure browser combo box is enabled/disabled appropriately
        self.methodChanged()

        self.parent = parent

    def okClicked(self):
        # Get needed references
        runningRecList = self.parent.runningRecList
        recID = self.ui.idLineEdit.text()

        # Check the list of running recorders to see if the identifier has already been used
        for i in range(len(runningRecList)):
            if runningRecList.item(i).text() == recID:
                # Show message if already used, and return
                QMessageBox.critical(self, "Duplicated identifier", "Another recorder already has that identifier."
                                                                    "Choose another identifier.")
                return

        # ID not used yet, so 'accept'. The main window will handle starting the new recorder and adding it to the list
        self.accept()

    def methodChanged(self):
        if self.ui.methodComboBox.currentText() in METHODS_USING_BROWSERS:
            self.ui.driverComboBox.setEnabled(True)
        else:
            self.ui.driverComboBox.setDisabled(True)


if __name__ == "__main__":
    app = QApplication([])

    dlg = AddRecorder()
    dlg.show()  # Windows are hidden by default

    app.exec()
