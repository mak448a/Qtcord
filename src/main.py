#! /usr/bin/env python3
import os

# Regenerate ui from ui file
os.system("pyside6-uic main.ui -o ui/main_ui.py")  # NOQA (basically tells pycharm to shut up)
os.system("pyside6-uic ui/login.ui -o ui/login_ui.py")  # NOQA

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton
)

from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets
import discord_integration

from discord_worker import Worker

from ui.main_ui import Ui_MainWindow
from login import LoginUI

# Will be set when run!
auth = False


class ChatInterface(QMainWindow, Ui_MainWindow):
    quit_shortcut = None
    response, prev_response = "", ""
    messages = ""
    friends = []
    guilds = []
    channel = 0

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        # Refresh interval used in setup function
        # Got "suspicious activity on your account" with this rate, let's try a different rate
        # self.refresh_message_interval = 600
        self.refresh_message_interval = 800

        self.setWindowIcon(QIcon("smiley.svg"))

        self.setup()

    def connect_signal_slots(self):
        self.ui.pushButton.clicked.connect(self.handle_input)

        self.ui.actionQuit.triggered.connect(quit)
        self.ui.actionAbout.triggered.connect(self.about)
        # Shortcuts
        # Quit
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_shortcut.activated.connect(quit)

        # Detect enter key by using event filter function from self.
        self.ui.lineEdit.returnPressed.connect(self.handle_input)

    def about(self):
        QMessageBox.about(
            self,
            "About QTCord",
            "<p>QTCord (c) mak448a 2023</p>"
            "<p>This app uses the following</p>"
            "<p>- PySide6</p>"
            "<p>- Qt Designer</p>"
            "<p>- <strong>Python</strong></p>"
            "<p>PySide is licensed under LGPL.</p>",
        )

    def handle_input(self):
        text = self.ui.lineEdit.text()
        if text:
            self.ui.lineEdit.setText("")

            self.messages += f"You: {text}\n"

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

        for message in messages:
            new_messages += message["username"] + ": " + message["content"] + "\n"

        if self.messages != new_messages:
            self.messages = new_messages
            self.ui.textBrowser.setText(self.messages)

            # Scroll to bottom
            self.ui.textBrowser.verticalScrollBar().setValue(self.ui.textBrowser.verticalScrollBar().maximum())

    def setup(self):
        self.connect_signal_slots()

        self.ui.lineEdit.setFocus()

        # Set timer to run every few ms to update the chat (8 seconds as we don't want banning)
        self.timer = QTimer()
        self.timer.setInterval(self.refresh_message_interval)
        self.timer.timeout.connect(self.update_messages)
        self.timer.start()

        def get_info():
            if auth:
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
            self.friends.append({
                "global_name": friend["user"]["global_name"],
                "channel": discord_integration.get_channel_from_id(friend["id"]),
                "nickname": friend["nickname"]
            })

        buttons = {}
        for i, friend in enumerate(self.friends):
            buttons[i] = QPushButton(text=friend["global_name"])
            self.ui.friends_tab.layout().addWidget(buttons[i])

            channel = friend["channel"]
            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            buttons[i].clicked.connect((lambda channel=channel: lambda: self.switch_channel(channel))(channel))

    def switch_channel(self, _id):
        self.channel = _id

    def get_servers(self):
        self.guilds = discord_integration.get_guilds()

        buttons = {}
        channel_buttons = {}

        for i, guild in enumerate(self.guilds):
            buttons[i] = QPushButton(text=guild["name"])
            self.ui.servers.layout().addWidget(buttons[i])

            # TODO: Get real stuff from discord_integration.get_guild_channels()
            # TODO: Only call this when you click on a channel, and switch the active tab too
            channel_buttons[i] = QPushButton(text=guild["name"])
            self.ui.channels.layout().addWidget(channel_buttons[i])

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            # buttons[i].clicked.connect((lambda channel=channel: lambda: self.switch_channel(channel))(channel))

    def get_channels(self, guild_id: int):
        channels = discord_integration.get_guild_channels(guild_id)

        buttons = {}
        for i, guild_id in enumerate(channels):
            buttons[i] = QPushButton(text=guild_id["name"])
            self.ui.servers.layout().addWidget(buttons[i])

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            # buttons[i].clicked.connect((lambda channel=channel: lambda: self.switch_channel(channel))(channel))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Add widget to switch between pages of UI
    widget = QtWidgets.QStackedWidget()

    if os.path.isfile("discordauth.txt"):
        with open("discordauth.txt") as f:
            if f.read():
                auth = True
                discord_integration.load_token()
            else:
                auth = False
    else:
        auth = False

    win = ChatInterface()
    login = LoginUI(widget)

    if not auth:
        widget.addWidget(login)

    widget.addWidget(win)

    # Set window properties
    widget.resize(840, 500)
    widget.setWindowTitle("QTCord")
    widget.setWindowIcon(QIcon("smiley.svg"))

    widget.show()
    sys.exit(app.exec())
