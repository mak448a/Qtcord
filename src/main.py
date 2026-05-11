#! /usr/bin/env python3
import os
import sys
import webbrowser
import requests
import platformdirs

import discord_integration
from discord_integration import keyring

# PySide imports
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets

# UI imports
from login import LoginUI
from chat_interface import ChatInterface
from version import get_version


# Will be set when run!
auth = False
current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")


def handle_no_internet() -> None:
    try:
        requests.get("https://discord.com")
    except requests.exceptions.ConnectionError:
        from no_internet import NoInternetUI

        app = QApplication(sys.argv)
        app.setDesktopFileName("io.github.mak448a.QTCord")
        NoInternetUI().exec()
        sys.exit(0)


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

    auth = False

    # Check keyring_available just in case. Probably redundant.
    if keyring.get_password("Qtcord", "token") and discord_integration.keyring_available:
        auth = True
    elif os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        print("Falling back to checking discordauth.txt")
        with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
            if f.read():
                auth = True

    win = ChatInterface(current_dir)
    win.menuBar().setNativeMenuBar(False)
    login = LoginUI(switcher)
    login.ui.howtologin.clicked.connect(
        lambda: webbrowser.open("https://github.com/mak448a/Qtcord/wiki/Logging-in-with-a-token")
    )

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
