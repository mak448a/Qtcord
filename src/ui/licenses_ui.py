# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'licenses.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import QDialogButtonBox, QGridLayout, QTextBrowser


class Ui_LicensesDialog(object):
    def setupUi(self, LicensesDialog):
        if not LicensesDialog.objectName():
            LicensesDialog.setObjectName("LicensesDialog")
        LicensesDialog.setWindowModality(Qt.WindowModality.WindowModal)
        LicensesDialog.resize(400, 300)
        self.gridLayout_2 = QGridLayout(LicensesDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QTextBrowser(LicensesDialog)
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(LicensesDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(LicensesDialog)
        self.buttonBox.accepted.connect(LicensesDialog.close)

        QMetaObject.connectSlotsByName(LicensesDialog)

    # setupUi

    def retranslateUi(self, LicensesDialog):
        LicensesDialog.setWindowTitle(
            QCoreApplication.translate("LicensesDialog", "Licenses", None)
        )
        self.textBrowser.setHtml(
            QCoreApplication.translate(
                "LicensesDialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:20pt; font-weight:700;">Qtcord Licenses</span></p>\n'
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:20pt; font-weight:700;\"><br /></p>\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; marg'
                'in-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Qtcord</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2023-present mak448a</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">PySide6</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">LGPL</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Platformdirs</span></p>\n'
                ""
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2010-202x The platformdirs developers</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Requests</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">Apache</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Python</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="'
                " font-family:'Noto Sans'; font-size:10pt;\">PSF</span></p>\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">xxHash</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">BSD: Copyright (c) 2012-2021 Yann Collet</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Altgraph</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2004 Istvan Albert unless otherwise noted., Copyright (c) 2006-2010 Bob Ippolito, Copyright'
                " (2) 2010-2020 Ronald Oussoren, et. al.</span></p>\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Certifi</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MPL</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Charset-Normalizer</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2019 TAHRI Ahmed R.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bloc'
                'k-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Idna</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">BSD: Copyright (c) 2013-2025, Kim Davies and contributors.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Urllib3</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2008-2020 Andrey Petrov and contributors.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:1'
                '0pt; font-weight:700;">Websocket-Client</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">Apache</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-weight:700;">Keyring (license copied from pip installation)</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">MIT: Copyright (c) 2025 &lt;copyright holders&gt;</span></p>\n'
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:10pt;\"><br /></p>\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt;">You can view the full licenses by going into the folder where Qtcord was installed. For Linux, check the following directories:</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-style:italic; text-decoration: underline;">/var/lib/flatpak/app/io.github.mak448a.QTCord/x86_64/stable/active/files/bin/licenses/</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Noto Sans\'; font-size:10pt; font-style:italic; text-decoration: underline;">~/.local/share/flatpak/app/io.github.mak448a.QTCord/x86_64/stable/active/files/bin/licenses/</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px'
                "; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:10pt; font-style:italic; text-decoration: underline;\"><br /></p></body></html>",
                None,
            )
        )

    # retranslateUi
