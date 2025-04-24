#! /usr/bin/env python3
import os
import sys
# import re
# import webbrowser
import requests
import platformdirs

# PySide imports
from PySide6.QtWidgets import QApplication #, QMainWindow, QMessageBox, QPushButton
from PySide6.QtGui import  QIcon #,  QShortcut, QKeySequence, QPixmap
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets
#from emoji import process_message_content


# from discord_workers import (
#     FileRequestWorker,
#     SendMessageWorker,
#     SendTypingWorker,
#     UpdateMessagesWorker,
# )
# import discord_integration

# UI imports
from ui.main_ui import Ui_MainWindow
from login import LoginUI
from licensesui import LicensesUI
from no_internet import NoInternetUI
from version import get_version

# Will be set when run!
auth = False
current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")

from mainWindow import ChatInterface 

def handle_no_internet() -> None:
    try:
        requests.get("https://discord.com")
    except requests.exceptions.ConnectionError:
        app = QApplication(sys.argv)
        app.setDesktopFileName("io.github.mak448a.QTCord")
        NoInternetUI().exec()
        sys.exit()


if __name__ == "__main__":
    # Get the version number for use in the about dialog and titlebar.
    version = get_version()
    # If no internet, throw up a dialog that says no internet
    handle_no_internet()

    # Make configuration and cache directories
    if not os.path.exists(platformdirs.user_config_dir("Qtcord")):
        os.makedirs(platformdirs.user_config_dir("Qtcord"))

    if not os.path.exists(platformdirs.user_cache_dir("Qtcord")):
        os.makedirs(platformdirs.user_cache_dir("Qtcord"))

    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.QTCord")

    # Add widget to switch between pages of UI
    switcher = QtWidgets.QStackedWidget()

    if os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
            if f.read():
                auth = True
            else:
                auth = False
    else:
        auth = False

    win = ChatInterface()
    login = LoginUI(switcher)

    switcher.addWidget(login)
    switcher.addWidget(win)
    if auth:
        switcher.setCurrentIndex(switcher.currentIndex() + 1)

    # Set window properties
    switcher.resize(840, 500)
    switcher.setWindowTitle(f"Qtcord {version}")
    icon_path = os.path.join(current_dir, "assets", "icon.svg")
    switcher.setWindowIcon(QIcon(icon_path))

    switcher.show()
    sys.exit(app.exec())
