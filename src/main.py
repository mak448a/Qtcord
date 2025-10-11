#! /usr/bin/env python3
import os
import sys
import platformdirs
import requests
from PySide6.QtWidgets import QApplication
from PySide6 import QtWidgets
from login import LoginUI
from no_internet import NoInternetUI
from version import get_version
from PySide6.QtGui import QIcon

from mainwindow import ChatInterface  # import the class

current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")

def handle_no_internet() -> None:
    try:
        requests.get("https://discord.com")
    except requests.exceptions.ConnectionError:
        app = QApplication(sys.argv)
        app.setDesktopFileName("io.github.mak448a.QTCord")
        NoInternetUI().exec()
        sys.exit()

if __name__ == "__main__":
    version = get_version()
    handle_no_internet()

    # Create config/cache directories
    if not os.path.exists(platformdirs.user_config_dir("Qtcord")):
        os.makedirs(platformdirs.user_config_dir("Qtcord"))

    if not os.path.exists(platformdirs.user_cache_dir("Qtcord")):
        os.makedirs(platformdirs.user_cache_dir("Qtcord"))

    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.QTCord")

    switcher = QtWidgets.QStackedWidget()

    auth_file = platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"
    auth = os.path.isfile(auth_file) and open(auth_file).read()

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
