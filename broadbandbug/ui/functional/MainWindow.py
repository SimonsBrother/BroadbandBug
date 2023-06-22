from broadbandbug.ui.mainwindow import Ui_MainWindow

from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # FUNCTIONALITY ASSIGNED HERE


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()  # Windows are hidden by default

    app.exec()
