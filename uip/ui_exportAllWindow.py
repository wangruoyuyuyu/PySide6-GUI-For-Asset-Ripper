# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportAllWindowEyEfgQ.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(606, 361)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_reset = QPushButton(Dialog)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setStyleSheet(u"QPushButton{\n"
"    padding-left:21px;\n"
"    padding-right:21px;\n"
"    padding-top:10.5px;\n"
"    padding-bottom:10.5px;\n"
"	background-color: rgb(220, 53, 69);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(187, 45, 59);\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.pushButton_reset)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(0, 30))

        self.verticalLayout.addWidget(self.lineEdit)

        self.checkBox_create_subdir = QCheckBox(Dialog)
        self.checkBox_create_subdir.setObjectName(u"checkBox_create_subdir")

        self.verticalLayout.addWidget(self.checkBox_create_subdir)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_export_project = QPushButton(Dialog)
        self.pushButton_export_project.setObjectName(u"pushButton_export_project")
        self.pushButton_export_project.setEnabled(False)
        self.pushButton_export_project.setStyleSheet(u"QPushButton{\n"
"    padding-left:21px;\n"
"    padding-right:21px;\n"
"    padding-top:10.5px;\n"
"    padding-bottom:10.5px;\n"
"	background-color: rgb(13, 110, 253);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(11, 94, 215);\n"
"}\n"
"QPushButton:disabled{\n"
"	color: rgb(175, 177, 180);\n"
"	background-color: rgb(43, 86, 180);\n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton_export_project)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_export_prim_content = QPushButton(Dialog)
        self.pushButton_export_prim_content.setObjectName(u"pushButton_export_prim_content")
        self.pushButton_export_prim_content.setEnabled(False)
        self.pushButton_export_prim_content.setStyleSheet(u"QPushButton{\n"
"    padding-left:21px;\n"
"    padding-right:21px;\n"
"    padding-top:10.5px;\n"
"    padding-bottom:10.5px;\n"
"	background-color: rgb(13, 110, 253);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(11, 94, 215);\n"
"}\n"
"QPushButton:disabled{\n"
"	color: rgb(175, 177, 180);\n"
"	background-color: rgb(43, 86, 180);\n"
"}")

        self.horizontalLayout_3.addWidget(self.pushButton_export_prim_content)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_sel_dir = QPushButton(Dialog)
        self.pushButton_sel_dir.setObjectName(u"pushButton_sel_dir")
        self.pushButton_sel_dir.setStyleSheet(u"QPushButton{\n"
"    padding-left:21px;\n"
"    padding-right:21px;\n"
"    padding-top:10.5px;\n"
"    padding-bottom:10.5px;\n"
"	background-color: rgb(25, 135, 84);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(21, 115, 71);\n"
"}")

        self.horizontalLayout_4.addWidget(self.pushButton_sel_dir)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_danger = QLabel(Dialog)
        self.label_danger.setObjectName(u"label_danger")
        self.label_danger.setStyleSheet(u"color: rgba(255, 255, 255, 0);")

        self.verticalLayout.addWidget(self.label_danger)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Export All", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.checkBox_create_subdir.setText(QCoreApplication.translate("Dialog", u"Create Subfolder", None))
        self.pushButton_export_project.setText(QCoreApplication.translate("Dialog", u"Export Unity Project", None))
        self.pushButton_export_prim_content.setText(QCoreApplication.translate("Dialog", u"Export Primary Content", None))
        self.pushButton_sel_dir.setText(QCoreApplication.translate("Dialog", u"Select Folder", None))
        self.label_danger.setText(QCoreApplication.translate("Dialog", u"Warning: this directory is not empty. All content will be deleted.\n"
"\n"
"", None))
    # retranslateUi

