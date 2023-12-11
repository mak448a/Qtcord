import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
import os
os.system("pyside6-uic test1.ui -o test1.py")
os.system("pyside6-uic test2.ui -o test2.py")
os.system("pyside6-uic login.ui -o login_ui.py")
import test1, test2, login_ui
from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QRunnable, Slot, QThreadPool
from PySide6 import QtWidgets




class MainWindow(QMainWindow, test1.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = test1.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.switch)
    
    def switch(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Win2(QMainWindow, login_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = login_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.switch)
    
    def switch(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()

    win2 = Win2()
    

    widget = QtWidgets.QStackedWidget()
    
    widget.addWidget(win)
    widget.addWidget(win2)
    
    widget.show()

    sys.exit(app.exec())
