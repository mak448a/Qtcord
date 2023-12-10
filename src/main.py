#! /usr/bin/env python3
import os
# Regenerate ui from ui file
os.system("pyside6-uic main.ui -o main_ui.py")  # NOQA (basically tells pycharm to shut up)

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)

from main_ui import Ui_MainWindow
from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QPushButton
import discord_integration
from PySide6.QtCore import QRunnable, Slot, QThreadPool
from discord_worker import Worker



class Window(QMainWindow, Ui_MainWindow):
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
        self.refresh_message_interval = 600
        
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
            "About ChatApp",
            "<p>ChatApp (c) mak448a 2023</p>"
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

        # Add friends to the UI
        self.get_friends()
        self.get_servers()

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
    win = Window()
    win.show()
    sys.exit(app.exec())
