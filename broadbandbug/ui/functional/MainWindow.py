from broadbandbug.ui.mainwindow import Ui_MainWindow
from broadbandbug.ui.functional.AddRecorder import AddRecorder
from broadbandbug.ui.functional.GraphColorDialog import GraphColorDialog
import broadbandbug.library.plotting as plotting
import broadbandbug.library.files as files

from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, results_csv_file, color_palette_json_path, threadpool=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE
        self.addRecBtn.clicked.connect(self.openAddRecDlg)
        self.stopRecBtn.clicked.connect(self.stopSelectedRec)
        self.showGraphBtn.clicked.connect(self.showGraph)
        self.changeColoursBtn.clicked.connect(self.changeGraphColors)

        self.color_palette_json_path = color_palette_json_path
        self.results_csv_file = results_csv_file

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
        from matplotlib import pyplot as plot
        plotting.styleGraph(plot)

        # Load results
        results = files.readResults(self.results_csv_file)
        colorPalettes = files.readPalette(self.color_palette_json_path)

        if self.separateCheckBox.isChecked():
            plotting.methodPlot(plot, results, colorPalettes)
        else:
            plotting.singlePlot(plot, results)

        plot.show()

    def changeGraphColors(self):
        dlg = GraphColorDialog(self.color_palette_json_path, self)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow("/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.csv",
                        "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.json")
    window.show()  # Windows are hidden by default

    app.exec()
