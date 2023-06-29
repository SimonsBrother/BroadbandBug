from broadbandbug.ui.mainwindow import Ui_MainWindow
from broadbandbug.ui.functional.AddRecorder import AddRecorder
from broadbandbug.ui.functional.GraphColorDialog import GraphColorDialog
import broadbandbug.library.plotting as plotting
import broadbandbug.library.files as files
from broadbandbug.library.classes import Recorder
from broadbandbug.methods.common import determineMethodFunction

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, results_csv_path: str, config_json_path: str, recorders: dict, tp_exe, results_queue, max_rec: int):
        """
        :param results_csv_path: path to the results csv file
        :param config_json_path: path to the config json file
        :param tp_exe: a ThreadPoolExecutor object
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE
        self.addRecBtn.clicked.connect(self.openAddRecDlg)
        self.stopRecBtn.clicked.connect(self.stopSelectedRec)
        self.showGraphBtn.clicked.connect(self.showGraph)
        self.changeColoursBtn.clicked.connect(self.changeGraphColors)

        self.config_json_path = config_json_path
        self.results_csv_file = results_csv_path
        self.tp_exe = tp_exe
        self.recorders = recorders
        self.results_queue = results_queue
        self.max_recorders = max_rec

    def openAddRecDlg(self):
        # Open the dialog for adding recorders
        dlg = AddRecorder(self)

        # Ensure max number of recorders isn't reached
        if len(self.recorders) < self.max_recorders:
            # Run dialog
            if dlg.exec():
                # If Ok clicked, add the identifier to list
                rec_id = dlg.ui.idLineEdit.text()
                self.runningRecList.addItem(rec_id)

                # Identify method function and browser to use
                rec_method = dlg.ui.methodComboBox.currentText()
                browser = dlg.ui.driverComboBox.currentText()
                function, params = determineMethodFunction(rec_method, browser)

                # Create new recorder
                new_recorder = Recorder(rec_id, function, params, self.results_queue)
                self.recorders[rec_id] = new_recorder

                # Start new recorder, adding it to thread pool
                new_recorder.startRecording(self.tp_exe)

        else:
            # Max recorders reached
            QMessageBox.critical(self, "Max recorders", f"The maximum number of recorders is {self.max_recorders}. "
                                                        f"Cannot add any more recorders.")

    def stopSelectedRec(self):
        # Check if there are any selected rows
        items = self.runningRecList.selectedIndexes()
        if len(items) > 0:
            # If so, confirm with message box
            msg_dlg = QMessageBox.question(self, "Confirmation", "Are you sure?")
            if msg_dlg == QMessageBox.StandardButton.Yes:
                # If confirmed, take (remove) the selected item from the row and get the identifier of the recorder to be stopped
                id_to_stop = self.runningRecList.takeItem(items[0].row()).text()
                # Stop the recorder
                self.recorders.pop(id_to_stop).stopRecording()

    def showGraph(self):
        from matplotlib import pyplot as plot
        plotting.styleGraph(plot)

        # Get date times to work with
        date_from = self.fromDTEdit.dateTime()
        date_to = self.toDTEdit.dateTime()

        # Load results
        results = files.readResults(self.results_csv_file, (date_from, date_to))
        color_palettes = files.readPalette(self.config_json_path)

        if self.separateCheckBox.isChecked():
            plotting.methodPlot(plot, results, color_palettes)
        else:
            plotting.singlePlot(plot, results)

        plot.show()

    def changeGraphColors(self):
        dlg = GraphColorDialog(self.config_json_path, self)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow("/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.csv",
                        "/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.json", {}, None, None, 2)
    window.show()  # Windows are hidden by default

    app.exec()
