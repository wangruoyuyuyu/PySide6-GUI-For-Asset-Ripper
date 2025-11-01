# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpen_File = QAction(MainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionOpen_Folder = QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(u"actionOpen_Folder")
        self.actionReset = QAction(MainWindow)
        self.actionReset.setObjectName(u"actionReset")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionHome = QAction(MainWindow)
        self.actionHome.setObjectName(u"actionHome")
        self.actionSettings_2 = QAction(MainWindow)
        self.actionSettings_2.setObjectName(u"actionSettings_2")
        self.actionConfiguration_Files = QAction(MainWindow)
        self.actionConfiguration_Files.setObjectName(u"actionConfiguration_Files")
        self.actionCommands = QAction(MainWindow)
        self.actionCommands.setObjectName(u"actionCommands")
        self.actionPrivacy = QAction(MainWindow)
        self.actionPrivacy.setObjectName(u"actionPrivacy")
        self.actionLicenses = QAction(MainWindow)
        self.actionLicenses.setObjectName(u"actionLicenses")
        self.actionOpenAPI_JSON = QAction(MainWindow)
        self.actionOpenAPI_JSON.setObjectName(u"actionOpenAPI_JSON")
        self.actionSwagger_Documentation = QAction(MainWindow)
        self.actionSwagger_Documentation.setObjectName(u"actionSwagger_Documentation")
        self.actionExport_All_Files = QAction(MainWindow)
        self.actionExport_All_Files.setObjectName(u"actionExport_All_Files")
        self.actionExport_All_Files.setEnabled(False)
        self.actionOriginal_UI = QAction(MainWindow)
        self.actionOriginal_UI.setObjectName(u"actionOriginal_UI")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.linkBtn1 = QPushButton(self.centralwidget)
        self.linkBtn1.setObjectName(u"linkBtn1")
        self.linkBtn1.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_4.addWidget(self.linkBtn1)

        self.linkBtn2 = QPushButton(self.centralwidget)
        self.linkBtn2.setObjectName(u"linkBtn2")
        self.linkBtn2.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_4.addWidget(self.linkBtn2)

        self.linkBtn3 = QPushButton(self.centralwidget)
        self.linkBtn3.setObjectName(u"linkBtn3")
        self.linkBtn3.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_4.addWidget(self.linkBtn3)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.linkBtn4 = QPushButton(self.centralwidget)
        self.linkBtn4.setObjectName(u"linkBtn4")
        self.linkBtn4.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.linkBtn4.setStyleSheet(u"border:none;\n"
"font: 9pt \"Microsoft YaHei UI\";\n"
"text-decoration: underline;color:rgb(119, 169, 255);")

        self.horizontalLayout_5.addWidget(self.linkBtn4)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.linkBtn5 = QPushButton(self.centralwidget)
        self.linkBtn5.setObjectName(u"linkBtn5")
        self.linkBtn5.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.linkBtn5.setStyleSheet(u"border:none;\n"
"font: 9pt \"Microsoft YaHei UI\";\n"
"text-decoration: underline;color:rgb(119, 169, 255);")

        self.horizontalLayout_5.addWidget(self.linkBtn5)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menu_Export = QMenu(self.menubar)
        self.menu_Export.setObjectName(u"menu_Export")
        self.menu_About = QMenu(self.menubar)
        self.menu_About.setObjectName(u"menu_About")
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(u"menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menu_Export.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.menu_File.addAction(self.actionOpen_File)
        self.menu_File.addAction(self.actionOpen_Folder)
        self.menu_File.addAction(self.actionReset)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionSettings)
        self.menuView.addAction(self.actionHome)
        self.menuView.addAction(self.actionSettings_2)
        self.menuView.addAction(self.actionConfiguration_Files)
        self.menuView.addAction(self.actionCommands)
        self.menuView.addAction(self.actionPrivacy)
        self.menuView.addAction(self.actionLicenses)
        self.menuView.addAction(self.actionOpenAPI_JSON)
        self.menuView.addAction(self.actionSwagger_Documentation)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionOriginal_UI)
        self.menu_Export.addAction(self.actionExport_All_Files)
        self.menu_About.addAction(self.action_About)
        self.menu_About.addAction(self.actionAbout_Qt)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Asset Ripper PySide6 GUI", None))
        self.actionOpen_File.setText(QCoreApplication.translate("MainWindow", u"&Open File", None))
        self.actionOpen_Folder.setText(QCoreApplication.translate("MainWindow", u"O&pen Folder", None))
        self.actionReset.setText(QCoreApplication.translate("MainWindow", u"&Reset", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.actionHome.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.actionSettings_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionConfiguration_Files.setText(QCoreApplication.translate("MainWindow", u"Configuration Files", None))
        self.actionCommands.setText(QCoreApplication.translate("MainWindow", u"Commands", None))
        self.actionPrivacy.setText(QCoreApplication.translate("MainWindow", u"Privacy", None))
        self.actionLicenses.setText(QCoreApplication.translate("MainWindow", u"Licenses", None))
        self.actionOpenAPI_JSON.setText(QCoreApplication.translate("MainWindow", u"OpenAPI JSON", None))
        self.actionSwagger_Documentation.setText(QCoreApplication.translate("MainWindow", u"Swagger Documentation", None))
        self.actionExport_All_Files.setText(QCoreApplication.translate("MainWindow", u"Export All Files", None))
        self.actionOriginal_UI.setText(QCoreApplication.translate("MainWindow", u"Original UI", None))
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About &Qt", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:28pt;\">Welcome</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"No Files Loaded", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"If you like AssetRipper, please consider donating:\n"
"\n"
"", None))
        self.linkBtn1.setText(QCoreApplication.translate("MainWindow", u"Patreon", None))
        self.linkBtn2.setText(QCoreApplication.translate("MainWindow", u"Paypal", None))
        self.linkBtn3.setText(QCoreApplication.translate("MainWindow", u"GitHub Sponsors", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"*These links are for the original project", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u00a9 2025 - PySide6-UI-for-AssetRipper - ", None))
        self.linkBtn4.setText(QCoreApplication.translate("MainWindow", u"Privacy", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u" - ", None))
        self.linkBtn5.setText(QCoreApplication.translate("MainWindow", u"Licenses", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_Export.setTitle(QCoreApplication.translate("MainWindow", u"&Export", None))
        self.menu_About.setTitle(QCoreApplication.translate("MainWindow", u"&About", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"&Language", None))
    # retranslateUi

