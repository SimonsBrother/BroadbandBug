from broadbandbug.ui.mainwindow import Ui_MainWindow
from broadbandbug.ui.functional.AddRecorder import AddRecorder
from broadbandbug.ui.functional.GraphColorDialog import GraphColorDialog

from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, threadpool=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE
        self.addRecBtn.clicked.connect(self.openAddRecDlg)
        self.stopRecBtn.clicked.connect(self.stopSelectedRec)
        self.showGraphBtn.clicked.connect(self.showGraph)
        self.changeColoursBtn.clicked.connect(self.changeGraphColors)

    def openAddRecDlg(self):
        # Open the dialog for adding recorders
        dlg = AddRecorder(self)

        # Run dialog
        if dlg.exec():
            # If Ok clicked, add the identifier to list
            recID = dlg.ui.idLineEdit.text()
            self.runningRecList.addItem(recID)

            # Make new recorder and add to threadpool
            recMethod = dlg.ui.methodComboBox.currentText()
            # todo add to thread pool

    def stopSelectedRec(self):
        ...

    def showGraph(self):
        ...

    def changeGraphColors(self):
        ...


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()  # Windows are hidden by default

    app.exec()
