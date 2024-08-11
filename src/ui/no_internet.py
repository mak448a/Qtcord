# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'no_internet.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_NoInternet(object):
    def setupUi(self, NoInternet):
        if not NoInternet.objectName():
            NoInternet.setObjectName(u"NoInternet")
        NoInternet.resize(400, 300)
        icon = QIcon(QIcon.fromTheme(u"io.github.mak448a.QTCord"))
        NoInternet.setWindowIcon(icon)
        self.gridLayout = QGridLayout(NoInternet)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser = QTextBrowser(NoInternet)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.retranslateUi(NoInternet)

        QMetaObject.connectSlotsByName(NoInternet)
    # setupUi

    def retranslateUi(self, NoInternet):
        NoInternet.setWindowTitle(QCoreApplication.translate("NoInternet", u"QTCord", None))
        self.textBrowser.setHtml(QCoreApplication.translate("NoInternet", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt; font-weight:700;\">Couldn't connect to Discord!</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">QTCord requires internet to connect to Discord.</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\">Either you aren't connected to a Wi-Fi network, or Discord is down.</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go to https://discordstatus.com/ to check if Discord is down.</p></body></html>", None))
    # retranslateUi

