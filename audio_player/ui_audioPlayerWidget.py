# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audioPlayerWidgetyfSOXK.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(827, 81)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_play = QPushButton(Form)
        self.pushButton_play.setObjectName(u"pushButton_play")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_play.sizePolicy().hasHeightForWidth())
        self.pushButton_play.setSizePolicy(sizePolicy)
        self.pushButton_play.setStyleSheet(u"font: 40pt \"Webdings\";")

        self.horizontalLayout.addWidget(self.pushButton_play)

        self.pushButton_stop = QPushButton(Form)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        sizePolicy.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy)
        self.pushButton_stop.setStyleSheet(u"font: 20pt \"Webdings\";")

        self.horizontalLayout.addWidget(self.pushButton_stop)

        self.label_status = QLabel(Form)
        self.label_status.setObjectName(u"label_status")

        self.horizontalLayout.addWidget(self.label_status)

        self.horizontalSlider = QSlider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_play.setText(QCoreApplication.translate("Form", u"4", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_stop.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p>g</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_stop.setText(QCoreApplication.translate("Form", u"g", None))
        self.label_status.setText(QCoreApplication.translate("Form", u"Not Loaded", None))
        self.label.setText(QCoreApplication.translate("Form", u"--:--:--", None))
    # retranslateUi

