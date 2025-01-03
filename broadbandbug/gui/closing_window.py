from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QDialog
from PyQt6.QtCore import QTimer

class ClosingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stopping recorders")

        # Main layout
        layout = QVBoxLayout()

        # Label to show message
        self.label = QLabel("Stopping running recorders...")
        layout.addWidget(self.label)

        # Set layout
        self.setLayout(layout)

        # Timer to close the window after 3 seconds
        QTimer.singleShot(3000, self.close)

        # Adjust window size
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

if __name__ == "__main__":
    app = QApplication([])
    dialog = ClosingDialog()
    dialog.show()
    app.exec()
