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

    def openAddRecDlg(self):
        dlg = AddRecorder(self)

        # Ok clicked
        if dlg.exec():
            # Make new recorder and add to threadpool
            recID = dlg.ui.idLineEdit.text()
            self.runningRecList.addItem(recID)

    def stopSelectedRec(self):
        ...


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()  # Windows are hidden by default

    app.exec()
