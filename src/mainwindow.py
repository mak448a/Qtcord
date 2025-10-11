#! /usr/bin/env python3
import os
import sys
import re
import webbrowser
from PySide6.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PySide6.QtGui import QShortcut, QKeySequence, QIcon, QPixmap
from PySide6.QtCore import QTimer, QThreadPool
from PySide6 import QtWidgets
from emoji import process_message_content

from discord_workers import FileRequestWorker, SendMessageWorker, SendTypingWorker, UpdateMessagesWorker
import discord_integration

from ui.main_ui import Ui_MainWindow
from licensesui import LicensesUI
import platformdirs
