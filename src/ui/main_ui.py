# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QGridLayout,
    QHBoxLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(840, 500)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionLicenses = QAction(MainWindow)
        self.actionLicenses.setObjectName(u"actionLicenses")
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName(u"actionLogout")
        self.actionReport_an_Issue = QAction(MainWindow)
        self.actionReport_an_Issue.setObjectName(u"actionReport_an_Issue")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 535, 408))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 840, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setMinimumSize(QSize(290, 221))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.friends_tab = QWidget()
        self.friends_tab.setObjectName(u"friends_tab")
        self.verticalLayout_4 = QVBoxLayout(self.friends_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea_2 = QScrollArea(self.friends_tab)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.friends_scrollArea_contents = QWidget()
        self.friends_scrollArea_contents.setObjectName(u"friends_scrollArea_contents")
        self.friends_scrollArea_contents.setGeometry(QRect(0, 0, 260, 381))
        self.verticalLayout_2 = QVBoxLayout(self.friends_scrollArea_contents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea_2.setWidget(self.friends_scrollArea_contents)

        self.verticalLayout_4.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.friends_tab, "")
        self.servers_tab = QWidget()
        self.servers_tab.setObjectName(u"servers_tab")
        self.horizontalLayout_5 = QHBoxLayout(self.servers_tab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.servers_notebook = QTabWidget(self.servers_tab)
        self.servers_notebook.setObjectName(u"servers_notebook")
        self.servers = QWidget()
        self.servers.setObjectName(u"servers")
        self.verticalLayout_6 = QVBoxLayout(self.servers)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.scrollArea_3 = QScrollArea(self.servers)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setMinimumSize(QSize(0, 0))
        self.scrollArea_3.setWidgetResizable(True)
        self.servers_scrollArea_contents = QWidget()
        self.servers_scrollArea_contents.setObjectName(u"servers_scrollArea_contents")
        self.servers_scrollArea_contents.setGeometry(QRect(0, 0, 237, 334))
        self.verticalLayout_5 = QVBoxLayout(self.servers_scrollArea_contents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea_3.setWidget(self.servers_scrollArea_contents)

        self.verticalLayout_6.addWidget(self.scrollArea_3)

        self.servers_notebook.addTab(self.servers, "")
        self.channels = QWidget()
        self.channels.setObjectName(u"channels")
        self.verticalLayout_7 = QVBoxLayout(self.channels)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.channels_scrollArea = QScrollArea(self.channels)
        self.channels_scrollArea.setObjectName(u"channels_scrollArea")
        self.channels_scrollArea.setWidgetResizable(True)
        self.channels_scrollArea_contents = QWidget()
        self.channels_scrollArea_contents.setObjectName(u"channels_scrollArea_contents")
        self.channels_scrollArea_contents.setGeometry(QRect(0, 0, 100, 30))
        self.verticalLayout_8 = QVBoxLayout(self.channels_scrollArea_contents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QTCord", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.actionLicenses.setText(QCoreApplication.translate("MainWindow", u"&Licenses", None))
        self.actionLogout.setText(QCoreApplication.translate("MainWindow", u"&Logout", None))
        self.actionReport_an_Issue.setText(QCoreApplication.translate("MainWindow", u"&Report an Issue", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No channel selected!</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.friends_tab), QCoreApplication.translate("MainWindow", u"Friends", None))
        self.servers_notebook.setTabText(self.servers_notebook.indexOf(self.servers), QCoreApplication.translate("MainWindow", u"Servers", None))
        self.servers_notebook.setTabText(self.servers_notebook.indexOf(self.channels), QCoreApplication.translate("MainWindow", u"Channels", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.servers_tab), QCoreApplication.translate("MainWindow", u"Servers", None))
    # retranslateUi

