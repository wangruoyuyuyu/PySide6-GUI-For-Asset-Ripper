# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cmdWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(642, 366)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))

        self.verticalLayout.addWidget(self.lineEdit)

        self.buttonBox_open = QDialogButtonBox(Dialog)
        self.buttonBox_open.setObjectName(u"buttonBox_open")
        self.buttonBox_open.setEnabled(False)
        self.buttonBox_open.setStyleSheet(u"QPushButton {\n"
"    padding-left: 21px; \n"
"    padding-right: 21px;\n"
"    padding-top: 10.5px;   \n"
"    padding-bottom: 10.5px; \n"
"	background-color: rgb(13, 110, 253);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:disabled{\n"
"	background-color: rgb(43, 86, 180);\n"
"	color: rgb(178, 179, 180);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(11, 94, 215);\n"
"}")
        self.buttonBox_open.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox_open.setStandardButtons(QDialogButtonBox.StandardButton.Open)
        self.buttonBox_open.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox_open)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_sel_file = QPushButton(Dialog)
        self.pushButton_sel_file.setObjectName(u"pushButton_sel_file")
        self.pushButton_sel_file.setStyleSheet(u"QPushButton {\n"
"    padding-left: 21px; \n"
"    padding-right: 21px;\n"
"    padding-top: 10.5px;   \n"
"    padding-bottom: 10.5px;\n"
"	background-color: rgb(25, 135, 84);\n"
"	color: rgb(255, 255, 255);\n"
" }\n"
"QPushButton:hover{\n"
"	background-color: rgb(21, 115, 71);\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_sel_file)

        self.pushButton_sel_folder = QPushButton(Dialog)
        self.pushButton_sel_folder.setObjectName(u"pushButton_sel_folder")
        self.pushButton_sel_folder.setStyleSheet(u"QPushButton {\n"
"    padding-left: 21px; \n"
"    padding-right: 21px;\n"
"    padding-top: 10.5px;   \n"
"    padding-bottom: 10.5px;\n"
"	background-color: rgb(25, 135, 84);\n"
"	color: rgb(255, 255, 255);\n"
" }\n"
"QPushButton:hover{\n"
"	background-color: rgb(21, 115, 71);\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_sel_folder)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Dialog)
        self.buttonBox_open.accepted.connect(Dialog.accept)
        self.buttonBox_open.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Commands", None))
        self.pushButton_sel_file.setText(QCoreApplication.translate("Dialog", u"Select File", None))
        self.pushButton_sel_folder.setText(QCoreApplication.translate("Dialog", u"Select Folder", None))
    # retranslateUi

