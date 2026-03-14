# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import (
    QDockWidget,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 500)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionLicenses = QAction(MainWindow)
        self.actionLicenses.setObjectName("actionLicenses")
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionReport_an_Issue = QAction(MainWindow)
        self.actionReport_an_Issue.setObjectName("actionReport_an_Issue")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.channel_label = QLabel(self.centralwidget)
        self.channel_label.setObjectName("channel_label")
        self.channel_label.setMargin(2)

        self.verticalLayout.addWidget(self.channel_label)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 535, 408))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 840, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidget.setMinimumSize(QSize(290, 221))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.friends_tab = QWidget()
        self.friends_tab.setObjectName("friends_tab")
        self.verticalLayout_4 = QVBoxLayout(self.friends_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea_2 = QScrollArea(self.friends_tab)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.friends_scrollArea_contents = QWidget()
        self.friends_scrollArea_contents.setObjectName("friends_scrollArea_contents")
        self.friends_scrollArea_contents.setGeometry(QRect(0, 0, 260, 32))
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.friends_scrollArea_contents.sizePolicy().hasHeightForWidth()
        )
        self.friends_scrollArea_contents.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.friends_scrollArea_contents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea_2.setWidget(self.friends_scrollArea_contents)

        self.verticalLayout_4.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.friends_tab, "")
        self.servers_tab = QWidget()
        self.servers_tab.setObjectName("servers_tab")
        self.horizontalLayout_5 = QHBoxLayout(self.servers_tab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.servers_notebook = QTabWidget(self.servers_tab)
        self.servers_notebook.setObjectName("servers_notebook")
        self.servers = QWidget()
        self.servers.setObjectName("servers")
        self.verticalLayout_6 = QVBoxLayout(self.servers)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scrollArea_3 = QScrollArea(self.servers)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollArea_3.setMinimumSize(QSize(0, 0))
        self.scrollArea_3.setWidgetResizable(True)
        self.servers_scrollArea_contents = QWidget()
        self.servers_scrollArea_contents.setObjectName("servers_scrollArea_contents")
        self.servers_scrollArea_contents.setGeometry(QRect(0, 0, 100, 30))
        sizePolicy.setHeightForWidth(
            self.servers_scrollArea_contents.sizePolicy().hasHeightForWidth()
        )
        self.servers_scrollArea_contents.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.servers_scrollArea_contents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea_3.setWidget(self.servers_scrollArea_contents)

        self.verticalLayout_6.addWidget(self.scrollArea_3)

        self.servers_notebook.addTab(self.servers, "")
        self.channels = QWidget()
        self.channels.setObjectName("channels")
        self.verticalLayout_7 = QVBoxLayout(self.channels)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.channels_scrollArea = QScrollArea(self.channels)
        self.channels_scrollArea.setObjectName("channels_scrollArea")
        self.channels_scrollArea.setWidgetResizable(True)
        self.channels_scrollArea_contents = QWidget()
        self.channels_scrollArea_contents.setObjectName("channels_scrollArea_contents")
        self.channels_scrollArea_contents.setGeometry(QRect(0, 0, 100, 30))
        sizePolicy.setHeightForWidth(
            self.channels_scrollArea_contents.sizePolicy().hasHeightForWidth()
        )
        self.channels_scrollArea_contents.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.channels_scrollArea_contents)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.channels_scrollArea.setWidget(self.channels_scrollArea_contents)

        self.verticalLayout_7.addWidget(self.channels_scrollArea)

        self.servers_notebook.addTab(self.channels, "")

        self.horizontalLayout_5.addWidget(self.servers_notebook)

        self.tabWidget.addTab(self.servers_tab, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionLicenses)
        self.menuHelp.addAction(self.actionReport_an_Issue)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.servers_notebook.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Qtcord", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "&About", None)
        )
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "&Quit", None))
        self.actionLicenses.setText(
            QCoreApplication.translate("MainWindow", "&Licenses", None)
        )
        self.actionLogout.setText(
            QCoreApplication.translate("MainWindow", "&Logout and Quit", None)
        )
        self.actionReport_an_Issue.setText(
            QCoreApplication.translate("MainWindow", "&Report an Issue", None)
        )
        self.channel_label.setText(
            QCoreApplication.translate("MainWindow", "Select a Channel to Start", None)
        )
        self.textBrowser.setPlainText(
            QCoreApplication.translate("MainWindow", "No channel selected!", None)
        )
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "Send", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "&File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "&Help", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.friends_tab),
            QCoreApplication.translate("MainWindow", "Friends", None),
        )
        self.servers_notebook.setTabText(
            self.servers_notebook.indexOf(self.servers),
            QCoreApplication.translate("MainWindow", "Servers", None),
        )
        self.servers_notebook.setTabText(
            self.servers_notebook.indexOf(self.channels),
            QCoreApplication.translate("MainWindow", "Channels", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.servers_tab),
            QCoreApplication.translate("MainWindow", "Servers", None),
        )

    # retranslateUi
