from PySide6.QtWidgets import QApplication, QDialog
from ui import licenses_ui
import sys


class LicensesUI(QDialog, licenses_ui.Ui_LicensesDialog):
    def __init__(self):
        super().__init__()

        self.ui = licenses_ui.Ui_LicensesDialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.QTCord")
    widget = LicensesUI()
    sys.exit(app.exec())
