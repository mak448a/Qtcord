#! /usr/bin/env python3
import os
import sys
import re
import webbrowser
import requests
import platformdirs

# PySide imports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PySide6.QtGui import QShortcut, QKeySequence, QIcon, QPixmap
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets

from discord_workers import (
    FileRequestWorker,
    SendMessageWorker,
    SendTypingWorker,
    UpdateMessagesWorker,
)
import discord_integration

# UI imports
from ui.main_ui import Ui_MainWindow
from login import LoginUI
from licensesui import LicensesUI
from no_internet import NoInternetUI
from version import get_version

# Will be set when run!
auth = False
current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")


class ChatInterface(QMainWindow, Ui_MainWindow):
    response, prev_response = "", ""
    messages = ""
    friends = []
    guilds = []
    channel_id = 0
    channel_buttons = []
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

            worker = SendMessageWorker(text, self.channel_id)
            worker.finished.connect(self.update_messages)
            self.threadpool.start(worker)

    def update_messages(self):
        # If we're not in a channel, stop immediately.
        if not self.channel_id:
            return

        worker = UpdateMessagesWorker(self.channel_id)
        worker.update.connect(self._update_text)
        self.threadpool.start(worker)

    def _update_text(self, messages: dict) -> None:
        if not self.channel_id:
            return

        # Get messages
        new_messages = ""
        last_timestamp = None

        for message in messages.get(self.channel_id, []):
            # Each message is a DiscordMessage object.

            # Here we're replacing <@user_id> with @username.
            # TODO: ALLOW SENDING @ MENTIONS
            if "<@" in message.content:
                matches = re.findall(r"<@(\d+)>", message.content)

                for id_mentioned in matches:
                    user = discord_integration.get_user_from_id(id_mentioned)
                    message.content = re.sub(
                        f"<@{id_mentioned}>",
                        f"<em>@{user.get_user_name()}</em>",
                        message.content,
                    )

            tags = """<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:700;">"""

            timestamp = message.timestamp
            if not last_timestamp or timestamp.day != last_timestamp.day:
                message_day = timestamp.strftime("%d %b %Y")
                new_messages += f"{tags}Day changed to {message_day}</span></p>\n"
            last_timestamp = timestamp

            message_hour = timestamp.strftime("%H:%M:%S")
            message_author = message.author.get_user_name()
            new_messages += f"{tags}[{message_hour}] {message_author}</span>: {message.content}</p>\n"

        if self.messages != new_messages and new_messages:
            self.messages = new_messages
            self.ui.textBrowser.setText(self.messages)

            # Scroll to bottom
            self.ui.textBrowser.verticalScrollBar().setValue(
                self.ui.textBrowser.verticalScrollBar().maximum()
            )

    def setup(self):
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
                self.get_guilds()
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
        self.friends = discord_integration.get_friends()

        for friend in self.friends:
            user = friend.user

            button = QPushButton(text=friend.get_user_name())

            def set_button_icon(button, data):
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    button.setIcon(QIcon(pixmap))

            if avatar_url := user.get_avatar_url():
                worker = FileRequestWorker(avatar_url, "users")
                worker.finished.connect(
                    (lambda button: lambda data: set_button_icon(button, data))(button)
                )
                self.threadpool.start(worker)

            default_avatar = os.path.join(current_dir, "assets", "user.png")
            button.setIcon(QIcon(default_avatar))

            self.ui.friends_scrollArea_contents.layout().addWidget(button)

            channel = discord_integration.get_channel_from_id(user.id)

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            button.clicked.connect(
                (lambda channel: lambda: self.switch_channel(channel))(channel)
            )

    def switch_channel(self, channel, guild_name=None):
        if channel.id != self.channel_id:
            self.channel_id = channel.id
            username = ""

            # TODO! Make this better for getting finding group DMs and finding the group name
            if 0 < len(channel.recipients) < 2:
                # This must be a one friend DM so get the user's nickname
                username = discord_integration.get_user_from_id(
                    channel.recipients[0].user.id, friend=True
                ).get_user_name()

            # Set the channel indicator label to the user's nickname or username depending
            self.ui.channel_label.setText(
                f"{guild_name + '>' if guild_name else ''}{username if username else channel.get_channel_name()}"
            )
            self.ui.textBrowser.setText("No messages in this conversation yet!")

    def get_guilds(self):
        self.guilds = discord_integration.get_guilds()

        for guild in self.guilds:
            button = QPushButton(text=guild.name)

            def set_button_icon(button, data):
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    button.setIcon(QIcon(pixmap))

            if icon_url := guild.get_icon_url():
                worker = FileRequestWorker(icon_url, "servers")
                worker.finished.connect(
                    (lambda button: lambda data: set_button_icon(button, data))(button)
                )
                self.threadpool.start(worker)

            default_icon = os.path.join(current_dir, "assets", "server.png")
            button.setIcon(QIcon(default_icon))

            self.ui.servers_scrollArea_contents.layout().addWidget(button)

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            button.clicked.connect(
                (lambda server: lambda: self.get_channels_in_guild(server))(guild)
            )

    def get_channels_in_guild(self, guild):
        # We want to change the tab to channels
        self.ui.servers_notebook.setCurrentIndex(1)

        # Clean buttons from previous server we visited
        for button in self.channel_buttons:
            button.deleteLater()

        self.channel_buttons = []

        # Dynamically add buttons based on channels
        for channel in discord_integration.get_guild_channels(guild.id):
            # Type 4 is a category and type 2 is a voice channel
            if channel.type == 4 or channel.type == 2:
                continue

            channel_name = channel.get_channel_name()
            if channel_name:
                button = QPushButton(text=channel_name)
            else:
                button = QPushButton(text="unamed-channel")

            self.ui.channels_scrollArea_contents.layout().addWidget(button)

            # Oh my headache do not touch this code.
            # But if you do: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
            button.clicked.connect(
                (
                    lambda channel: lambda: self.switch_channel(
                        channel, guild_name=guild.name
                    )
                )(channel)
            )

            self.channel_buttons.append(button)

    def send_typing(self):
        # Called every time we change the text.
        if not self.channel_id:
            return

        if 0 < len(self.ui.lineEdit.text()) < 2:
            worker = SendTypingWorker(self.channel_id)
            self.threadpool.start(worker)

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
    switcher.setWindowTitle(f"Qtcord {version}")
    icon_path = os.path.join(current_dir, "assets", "icon.svg")
    switcher.setWindowIcon(QIcon(icon_path))

    switcher.show()
    sys.exit(app.exec())
