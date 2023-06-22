from broadbandbug.ui.graphcolordialog import Ui_GraphColorDialog

from PyQt6.QtWidgets import QApplication, QDialog


# Adapted from https://www.pythonguis.com/tutorials/pyqt6-creating-dialogs-qt-designer/
class GraphColorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_GraphColorDialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE


if __name__ == "__main__":
    app = QApplication([])

    dlg = GraphColorDialog()
    dlg.show()  # Windows are hidden by default

    app.exec()
