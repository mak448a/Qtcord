#! /usr/bin/env python3
import os
import sys
import webbrowser
import requests

# PySide imports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets

# 3rd party libraries
import platformdirs

from discord_worker import Worker
import discord_integration
import discord_status

# UI imports
from ui.main_ui import Ui_MainWindow
from login import LoginUI
from licensesui import LicensesUI
from no_internet import NoInternetUI

# Will be set when run!
auth = False
current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")


class ChatInterface(QMainWindow, Ui_MainWindow):
    response, prev_response = "", ""
    messages = ""
    friends = []
    guilds = []
    channel = 0
    channel_buttons = {}
    typing = False

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        # Refresh interval used in setup function
        # Got "suspicious activity on your account" with this rate, let's try a different rate
        # self.refresh_message_interval = 600
        self.refresh_message_interval = 1000
        icon_path = os.path.join(current_dir, "assets", "icon.svg")
        self.setWindowIcon(QIcon(icon_path))

        self.setup()

    def connect_signal_slots(self):
        # Connect buttons to actions
        self.ui.pushButton.clicked.connect(self.handle_input)

        # Connect menubar actions
        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionLicenses.triggered.connect(self.display_licenses)
        self.ui.actionLogout.triggered.connect(self.logout_account)
        self.ui.actionReport_an_Issue.triggered.connect(self.open_issues)

        # Shortcuts
        # Quit
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_shortcut.activated.connect(sys.exit)

        # Detect enter key by using event filter function from self.
        self.ui.lineEdit.textChanged.connect(self.send_typing)
        self.ui.lineEdit.returnPressed.connect(self.handle_input)

    def open_issues(self):
        webbrowser.open("https://github.com/mak448a/Qtcord")

    def about(self):
        QMessageBox.about(
            self,
            "About Qtcord",
            "<p>Qtcord (c) mak448a 2023-2024</p>"
            "<p>This app was built with the following:</p>"
            "<p>- PySide6</p>"
            "<p>- Python</p>"
            "<p>- Requests</p>",
        )

    def display_licenses(self):
        LicensesUI().exec()

    def handle_input(self):
        text = self.ui.lineEdit.text()
        if text:
            self.ui.lineEdit.setText("")

            discord_integration.send_message(text, self.channel)

            self.update_messages()

    def update_messages(self):
        # If we're not in a channel, stop immediately.
        if not self.channel:
            return

        worker = Worker(self.channel)
        worker.signals.update.connect(self._update_text)
        self.threadpool.start(worker)

    def _update_text(self, messages):
        if not self.channel:
            return

        # Get messages
        new_messages = ""
        last_timestamp = None

        for message in messages.get(self.channel, []):
            tags = """<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:700;">"""

            timestamp = message["timestamp"]
            if not last_timestamp or timestamp.day != last_timestamp.day:
                message_day = timestamp.strftime("%d %b %Y")
                new_messages += f"{tags}Day changed to {message_day}</span></p>\n"
            last_timestamp = timestamp

            message_hour = timestamp.strftime("%H:%M:%S")
            new_messages += f"{tags}[{message_hour}] {message['username']}</span>: {message['content']}</p>\n"

        if self.messages != new_messages and new_messages:
            self.messages = new_messages
            self.ui.textBrowser.setText(self.messages)

            # Scroll to bottom
            self.ui.textBrowser.verticalScrollBar().setValue(
                self.ui.textBrowser.verticalScrollBar().maximum()
            )

    def setup(self):
        if auth:
            discord_status.keep_online()

        self.connect_signal_slots()

        self.ui.lineEdit.setFocus()

        # Set timer to run every few ms to update the chat (8 seconds as we don't want banning)
        self.timer = QTimer()
        self.timer.setInterval(self.refresh_message_interval)
        self.timer.timeout.connect(self.update_messages)
        self.timer.start()

        def get_info():
            if os.path.isfile(
                platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"
            ):
                with open(
                    platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"
                ) as f:
                    if f.read():
                        auth2 = True
                        discord_integration.load_token()
                    else:
                        auth2 = False
            else:
                auth2 = False

            if auth2:
                self.get_friends()
                self.get_servers()
                self.timer2.setSingleShot(True)
                # This gets called anyway, tell IDE to ignore
                self.timer2.stop()

        self.timer2 = QTimer()
        self.timer2.setInterval(800)
        self.timer2.timeout.connect(get_info)
        self.timer2.start()

        # Add friends to the UI
        get_info()

    def get_friends(self):
        for friend in discord_integration.get_friends():
            self.friends.append(
                {
                    "global_name": friend["user"]["global_name"],
                    "user_id": friend["id"],
                    "channel": discord_integration.get_channel_from_id(friend["id"]),
                    "nickname": friend["nickname"],
                }
            )

        buttons = {}
        for i, friend in enumerate(self.friends):
            buttons[i] = QPushButton(text=friend["global_name"])

            if os.path.exists(
                os.path.join(
                    platformdirs.user_cache_dir("Qtcord"),
                    "users",
                    f"{friend['user_id']}.webp",
                )
            ):
                icon = QIcon(
                    os.path.join(
                        platformdirs.user_cache_dir("Qtcord"),
                        "users",
                        f"{friend['user_id']}.webp",
                    )
                )
            else:
                icon = QIcon(os.path.join(current_dir, "assets", "user.png"))

            buttons[i].setIcon(icon)
            self.ui.friends_scrollArea_contents.layout().addWidget(buttons[i])

            channel = friend["channel"]
            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            buttons[i].clicked.connect(
                (lambda channel=channel: lambda: self.switch_channel(channel))(channel)
            )

    def switch_channel(self, _id):
        if _id != self.channel:
            self.channel = _id
            self.ui.textBrowser.setText("No messages in this conversation yet!")

    def get_servers(self):
        self.guilds = discord_integration.get_guilds()

        buttons = {}

        for i, guild in enumerate(self.guilds):
            buttons[i] = QPushButton(text=guild["name"])

            if os.path.exists(
                os.path.join(
                    platformdirs.user_cache_dir("Qtcord"),
                    "servers",
                    f"{guild['id']}.png",
                )
            ):
                icon = QIcon(
                    os.path.join(
                        platformdirs.user_cache_dir("Qtcord"),
                        "servers",
                        f"{guild['id']}.png",
                    )
                )
            else:
                icon = QIcon(os.path.join(current_dir, "assets", "server.png"))

            buttons[i].setIcon(icon)
            self.ui.servers_scrollArea_contents.layout().addWidget(buttons[i])

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            buttons[i].clicked.connect(
                (lambda server=guild: lambda: self.get_channels_in_guild(server))(guild)
            )

    def get_channels_in_guild(self, guild):
        # We want to change the tab to channels
        self.ui.servers_notebook.setCurrentIndex(1)
        channels = discord_integration.get_guild_channels(guild["id"])

        # Clean buttons from previous server we visited
        for button in self.channel_buttons:
            self.channel_buttons[button].deleteLater()

        self.channel_buttons = {}

        # Dynamically add buttons based on channels
        for i, channel in enumerate(channels):
            # Type 4 is a category and type 2 is a voice channel
            if channel["type"] == 4 or channel["type"] == 2:
                continue
            self.channel_buttons[i] = QPushButton(text=channel["name"])
            self.ui.channels_scrollArea_contents.layout().addWidget(
                self.channel_buttons[i]
            )

            # channel_buttons[i] = QPushButton(text=guild["name"])
            # self.ui.channels.layout().addWidget(channel_buttons[i])
            channel_id = channel["id"]
            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            self.channel_buttons[i].clicked.connect(
                (lambda _id=channel_id: lambda: self.switch_channel(_id))(channel_id)
            )

    def get_channels(self, guild_id: int):
        channels = discord_integration.get_guild_channels(guild_id)

        buttons = {}
        for i, guild in enumerate(channels):
            buttons[i] = QPushButton(text=guild["name"])
            self.ui.servers.layout().addWidget(buttons[i])

    def send_typing(self):
        # Called every time we change the text.
        if not self.channel:
            return

        if 0 < len(self.ui.lineEdit.text()) < 2:
            discord_integration.send_typing(self.channel)

    def logout_account(self):
        # Remove Discord token from discordauth.txt
        os.remove(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt")
        # Exit the app
        sys.exit(0)


def handle_no_internet() -> None:
    try:
        requests.get("https://discord.com")
    except requests.exceptions.ConnectionError:
        app = QApplication(sys.argv)
        app.setDesktopFileName("io.github.mak448a.Qtcord")
        NoInternetUI().exec()
        sys.exit()


if __name__ == "__main__":
    # If no internet, throw up a dialog that says no internet
    handle_no_internet()

    # Make configuration and cache directories
    if not os.path.exists(platformdirs.user_config_dir("Qtcord")):
        os.makedirs(platformdirs.user_config_dir("Qtcord"))

    if not os.path.exists(platformdirs.user_cache_dir("Qtcord")):
        os.makedirs(platformdirs.user_cache_dir("Qtcord"))

    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.Qtcord")

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
    switcher.setWindowTitle("Qtcord")
    icon_path = os.path.join(current_dir, "assets", "icon.svg")
    switcher.setWindowIcon(QIcon(icon_path))

    switcher.show()
    sys.exit(app.exec())
