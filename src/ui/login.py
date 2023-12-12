from PySide6.QtWidgets import QMainWindow
from . import login_ui


class LoginUI(QMainWindow, login_ui.Ui_MainWindow):
    def __init__(self, switcher, parent=None):
        super().__init__(parent)

        self.ui = login_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.switch)
        self.switcher = switcher
    
    def switch(self):
        print("Get the discord token pleaselol")
        self.switcher.setCurrentIndex(self.switcher.currentIndex() + 1)
