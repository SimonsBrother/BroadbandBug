from broadbandbug.ui.graphcolordialog import Ui_GraphColorDialog
from broadbandbug.library.constants import SUPPORTED_METHODS
from broadbandbug.library.files import writePalette, readPalette

from PyQt6.QtWidgets import QApplication, QDialog, QColorDialog


def coloredBlocks(color="000000", count=3):
    return f'<html><head/><body><p><span style=" color:#{str(color)};">{"█" * count}</span></p></body></html>'


# Adapted from https://www.pythonguis.com/tutorials/pyqt6-creating-dialogs-qt-designer/
class GraphColorDialog(QDialog):
    def __init__(self, palette_json_path, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_GraphColorDialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE
        # Load color palette as an attribute
        self.colorPalette = readPalette(palette_json_path)
        self.palette_json_path = palette_json_path

        # Add possible methods to combo box
        self.ui.methodComboBox.addItems(SUPPORTED_METHODS)
        # Load first method
        firstMethodPalette = self.colorPalette[self.ui.methodComboBox.currentText()]
        self.ui.downSampleLabel.setText(coloredBlocks(firstMethodPalette['download']))
        self.ui.upSampleLabel.setText(coloredBlocks(firstMethodPalette['upload']))

        # Assign function to buttons and combo box
        self.ui.downEditBtn.clicked.connect(self.editDownColor)
        self.ui.upEditBtn.clicked.connect(self.editUpColor)
        self.ui.saveBtn.clicked.connect(self.saveColors)
        self.ui.methodComboBox.currentIndexChanged.connect(self.loadSelectedPalette)

    def openColorDlg(self):
        """ Opens a QColorDialog, returns None if cancelled, returns color as hex value otherwise """
        colorDlg = QColorDialog(self)

        if colorDlg.exec():
            # Get color as tuple of red, green, blue, and alpha
            rgbColor = colorDlg.selectedColor().getRgb()

            # Convert to string storing colors as hex values, ignoring alpha, and removing 0x from the converted values
            rgbHexes = [hex(rgbColor[0]).removeprefix("0x"),
                        hex(rgbColor[1]).removeprefix("0x"),
                        hex(rgbColor[2]).removeprefix("0x")]

            # Iterate over each value and add 0 to start so that each value is at least 2 digits
            for i in range(len(rgbHexes)):
                if len(rgbHexes[i]) == 1:
                    rgbHexes[i] = f"0{rgbHexes[i]}"

            # Merge hex values into 1 string
            hexColor = rgbHexes[0] + rgbHexes[1] + rgbHexes[2]

            return hexColor

        # Cancel
        return None

    def editDownColor(self):
        # Get color
        color = self.openColorDlg()

        # If GUI was not cancelled
        if color:
            # Change color of palette attribute of GUI
            self.colorPalette[self.ui.methodComboBox.currentText()]["download"] = color
            self.ui.downSampleLabel.setText(coloredBlocks(color))

    def editUpColor(self):
        # Get color
        color = self.openColorDlg()

        # If GUI was not cancelled
        if color:
            # Change color of palette attribute of GUI
            self.colorPalette[self.ui.methodComboBox.currentText()]["upload"] = color
            self.ui.upSampleLabel.setText(coloredBlocks(color))

    def saveColors(self):
        writePalette(self.palette_json_path, self.colorPalette)

    def loadSelectedPalette(self):
        """ Reloads color palettes from json, and loads the selected method's palette into sample """
        self.colorPalette = readPalette(self.palette_json_path)
        methodPalette = self.colorPalette[self.ui.methodComboBox.currentText()]
        self.ui.downSampleLabel.setText(coloredBlocks(methodPalette['download']))
        self.ui.upSampleLabel.setText(coloredBlocks(methodPalette['upload']))



if __name__ == "__main__":
    app = QApplication([])

    dlg = GraphColorDialog("/Users/calebhair/Documents/Projects/BroadbandBug/broadbandbug/tests/test.json")
    dlg.show()  # Windows are hidden by default

    app.exec()
