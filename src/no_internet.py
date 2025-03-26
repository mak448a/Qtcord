from ui.no_internet import Ui_NoInternet
from PySide6.QtWidgets import QApplication, QDialog
import sys


class NoInternetUI(QDialog, Ui_NoInternet):
    def __init__(self):
        super().__init__()

        self.ui = Ui_NoInternet()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.QTCord")
    widget = NoInternetUI()
    sys.exit(app.exec())
