# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetWindow.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

from audio_player import AudioPlayerWidget
from glb_viewer import GLBViewerWidget
from network_image_loader import ReliableImageScaler
from network_video_player import VLCVideoWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(677, 410)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = QLabel(Dialog)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"font: 26pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.label_title)

        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget_info = QTableWidget(self.tab)
        self.tableWidget_info.setObjectName(u"tableWidget_info")

        self.verticalLayout_2.addWidget(self.tableWidget_info)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_audioplay = AudioPlayerWidget(self.tab_2)
        self.widget_audioplay.setObjectName(u"widget_audioplay")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_audioplay.sizePolicy().hasHeightForWidth())
        self.widget_audioplay.setSizePolicy(sizePolicy)
        self.widget_audioplay.setMinimumSize(QSize(0, 50))
        self.widget_audioplay.setBaseSize(QSize(0, 1000))

        self.verticalLayout_3.addWidget(self.widget_audioplay)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)

        self.pushButton_save_audio = QPushButton(self.tab_2)
        self.pushButton_save_audio.setObjectName(u"pushButton_save_audio")

        self.horizontalLayout_7.addWidget(self.pushButton_save_audio)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_image = ReliableImageScaler(self.tab_3)
        self.widget_image.setObjectName(u"widget_image")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_image.sizePolicy().hasHeightForWidth())
        self.widget_image.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.widget_image)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_saveimage = QPushButton(self.tab_3)
        self.pushButton_saveimage.setObjectName(u"pushButton_saveimage")

        self.horizontalLayout.addWidget(self.pushButton_saveimage)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_modelpreview = GLBViewerWidget(self.tab_4)
        self.widget_modelpreview.setObjectName(u"widget_modelpreview")
        sizePolicy1.setHeightForWidth(self.widget_modelpreview.sizePolicy().hasHeightForWidth())
        self.widget_modelpreview.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.widget_modelpreview)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_14)

        self.pushButton_save_model = QPushButton(self.tab_4)
        self.pushButton_save_model.setObjectName(u"pushButton_save_model")

        self.horizontalLayout_8.addWidget(self.pushButton_save_model)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_13)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_6 = QVBoxLayout(self.tab_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.textEdit = QTextEdit(self.tab_5)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_6.addWidget(self.textEdit)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_15)

        self.pushButton_save_text = QPushButton(self.tab_5)
        self.pushButton_save_text.setObjectName(u"pushButton_save_text")

        self.horizontalLayout_9.addWidget(self.pushButton_save_text)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_16)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_7 = QVBoxLayout(self.tab_6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.webEngineView_fontpreview = QWebEngineView(self.tab_6)
        self.webEngineView_fontpreview.setObjectName(u"webEngineView_fontpreview")
        self.webEngineView_fontpreview.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_7.addWidget(self.webEngineView_fontpreview)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButton_save_font = QPushButton(self.tab_6)
        self.pushButton_save_font.setObjectName(u"pushButton_save_font")

        self.horizontalLayout_2.addWidget(self.pushButton_save_font)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout_8 = QVBoxLayout(self.tab_7)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_video_play = VLCVideoWidget(self.tab_7)
        self.widget_video_play.setObjectName(u"widget_video_play")
        sizePolicy1.setHeightForWidth(self.widget_video_play.sizePolicy().hasHeightForWidth())
        self.widget_video_play.setSizePolicy(sizePolicy1)

        self.verticalLayout_8.addWidget(self.widget_video_play)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_playprogress = QLabel(self.tab_7)
        self.label_playprogress.setObjectName(u"label_playprogress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_playprogress.sizePolicy().hasHeightForWidth())
        self.label_playprogress.setSizePolicy(sizePolicy2)
        self.label_playprogress.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_6.addWidget(self.label_playprogress)

        self.horizontalSlider_playprogress = QSlider(self.tab_7)
        self.horizontalSlider_playprogress.setObjectName(u"horizontalSlider_playprogress")
        self.horizontalSlider_playprogress.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.horizontalSlider_playprogress)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.pushButton_savevdo = QPushButton(self.tab_7)
        self.pushButton_savevdo.setObjectName(u"pushButton_savevdo")

        self.horizontalLayout_5.addWidget(self.pushButton_savevdo)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_9 = QVBoxLayout(self.tab_8)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.textEdit_yaml = QTextEdit(self.tab_8)
        self.textEdit_yaml.setObjectName(u"textEdit_yaml")

        self.verticalLayout_9.addWidget(self.textEdit_yaml)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.pushButton_save_yaml = QPushButton(self.tab_8)
        self.pushButton_save_yaml.setObjectName(u"pushButton_save_yaml")

        self.horizontalLayout_3.addWidget(self.pushButton_save_yaml)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_10 = QVBoxLayout(self.tab_9)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit_json = QTextEdit(self.tab_9)
        self.textEdit_json.setObjectName(u"textEdit_json")

        self.verticalLayout_10.addWidget(self.textEdit_json)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.pushButton_save_json = QPushButton(self.tab_9)
        self.pushButton_save_json.setObjectName(u"pushButton_save_json")

        self.horizontalLayout_4.addWidget(self.pushButton_save_json)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.verticalLayout_10.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab_9, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.label = QLabel(self.tab_10)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 391, 81))
        self.label.setStyleSheet(u"font: 28pt \"Microsoft YaHei UI\";")
        self.label_2 = QLabel(self.tab_10)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 561, 31))
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.verticalLayout_11 = QVBoxLayout(self.tab_11)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.tableWidget_dependencies = QTableWidget(self.tab_11)
        self.tableWidget_dependencies.setObjectName(u"tableWidget_dependencies")

        self.verticalLayout_11.addWidget(self.tableWidget_dependencies)

        self.tabWidget.addTab(self.tab_11, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.verticalLayout_12 = QVBoxLayout(self.tab_12)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tableWidget_development = QTableWidget(self.tab_12)
        self.tableWidget_development.setObjectName(u"tableWidget_development")

        self.verticalLayout_12.addWidget(self.tableWidget_development)

        self.tabWidget.addTab(self.tab_12, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Loaded Assets", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Information", None))
        self.pushButton_save_audio.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Audio", None))
        self.pushButton_saveimage.setText(QCoreApplication.translate("Dialog", u"Save Raw Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Image", None))
        self.pushButton_save_model.setText(QCoreApplication.translate("Dialog", u"Save GLB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"Model", None))
        self.pushButton_save_text.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Text", None))
        self.pushButton_save_font.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("Dialog", u"Font", None))
        self.label_playprogress.setText("")
        self.pushButton_savevdo.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("Dialog", u"Video", None))
        self.pushButton_save_yaml.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QCoreApplication.translate("Dialog", u"Yaml", None))
        self.pushButton_save_json.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), QCoreApplication.translate("Dialog", u"Json", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"not implemented", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Because of the shortage of testing files,I'm sorry that this function is not implenmented now.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), QCoreApplication.translate("Dialog", u"Hex", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), QCoreApplication.translate("Dialog", u"Dependencies", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_12), QCoreApplication.translate("Dialog", u"Development", None))
    # retranslateUi

