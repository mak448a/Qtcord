#! /usr/bin/env python3
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")  # NOQA (basically tells pycharm to shut up)

# Regenerate ui from ui files
if os.path.exists(f"{os.path.expanduser('~/Documents/regenerate_ui_files_indicator.txt')}"):  # NOQA
    os.system(f"pyside6-uic {current_dir}/ui/main.ui -o {current_dir}/ui/main_ui.py")  # NOQA
    os.system(f"pyside6-uic {current_dir}/ui/login.ui -o {current_dir}/ui/login_ui.py")  # NOQA
    os.system(f"pyside6-uic {current_dir}/ui/licenses.ui -o {current_dir}/ui/licenses_ui.py")  # NOQA


# Pyside imports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton
)

from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets
import platformdirs

from discord_worker import Worker
import discord_integration

# UI imports
from ui.main_ui import Ui_MainWindow
from login import LoginUI
from licenses import LicensesUI

# Will be set when run!
auth = False


class ChatInterface(QMainWindow, Ui_MainWindow):
    response, prev_response = "", ""
    messages = ""
    friends = []
    guilds = []
    channel = 0
    channel_buttons = {}
    typing = False

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        # Refresh interval used in setup function
        # Got "suspicious activity on your account" with this rate, let's try a different rate
        # self.refresh_message_interval = 600
        self.refresh_message_interval = 1000
        icon_path = os.path.join(current_dir, "assets", "smiley.svg")
        self.setWindowIcon(QIcon(icon_path))

        self.setup()

    def connect_signal_slots(self):
        self.ui.pushButton.clicked.connect(self.handle_input)

        self.ui.actionQuit.triggered.connect(sys.exit)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionLicenses.triggered.connect(self.display_licenses)
        # Shortcuts
        # Quit
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_shortcut.activated.connect(sys.exit)

        # Detect enter key by using event filter function from self.
        self.ui.lineEdit.textChanged.connect(self.send_typing)
        self.ui.lineEdit.returnPressed.connect(self.handle_input)

    def about(self):
        QMessageBox.about(
            self,
            "About QTCord",
            "<p>QTCord (c) mak448a 2023-2024</p>"
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

        if self.messages != new_messages and new_messages:
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
            if os.path.isfile(platformdirs.user_config_dir("QTCord") + "/discordauth.txt"):
                with open(platformdirs.user_config_dir("QTCord") + "/discordauth.txt") as f:
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
            self.friends.append({
                "global_name": friend["user"]["global_name"],
                "channel": discord_integration.get_channel_from_id(friend["id"]),
                "nickname": friend["nickname"]
            })

        buttons = {}
        for i, friend in enumerate(self.friends):
            buttons[i] = QPushButton(text=friend["global_name"])
            self.ui.friends_scrollArea_contents.layout().addWidget(buttons[i])

            channel = friend["channel"]
            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            buttons[i].clicked.connect((lambda channel=channel: lambda: self.switch_channel(channel))(channel))

    def switch_channel(self, _id):
        self.channel = _id
        self.ui.textBrowser.setText("No messages in this conversation yet!")

    def get_servers(self):
        self.guilds = discord_integration.get_guilds()

        buttons = {}

        for i, guild in enumerate(self.guilds):
            buttons[i] = QPushButton(text=guild["name"])
            self.ui.servers_scrollArea_contents.layout().addWidget(buttons[i])

            # TODO: Get real stuff from discord_integration.get_guild_channels()
            # TODO: Only call this when you click on a channel, and switch the active tab too
            # channel_buttons[i] = QPushButton(text=guild["name"])
            # self.ui.channels.layout().addWidget(channel_buttons[i])

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            buttons[i].clicked.connect((lambda server=guild: lambda: self.get_channels_in_guild(server))(guild))

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
            self.ui.channels_scrollArea_contents.layout().addWidget(self.channel_buttons[i])

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
        for i, guild_id in enumerate(channels):
            buttons[i] = QPushButton(text=guild_id["name"])
            self.ui.servers.layout().addWidget(buttons[i])

    def send_typing(self):
        # Called every time we change the text.
        if not self.channel:
            return
        
        if 0 < len(self.ui.lineEdit.text()) < 2:
            discord_integration.send_typing(self.channel)



if __name__ == "__main__":
    if not os.path.exists(platformdirs.user_config_dir("QTCord")):
        os.makedirs(platformdirs.user_config_dir("QTCord"))
    app = QApplication(sys.argv)
    app.setDesktopFileName("io.github.mak448a.QTCord")
    
    # Add widget to switch between pages of UI
    widget = QtWidgets.QStackedWidget()

    if os.path.isfile(platformdirs.user_config_dir("QTCord") + "/discordauth.txt"):
        with open(platformdirs.user_config_dir("QTCord") + "/discordauth.txt") as f:
            if f.read():
                auth = True
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
    icon_path = os.path.join(current_dir, "assets", "smiley.svg")
    widget.setWindowIcon(QIcon(icon_path))

    widget.show()
    sys.exit(app.exec())
