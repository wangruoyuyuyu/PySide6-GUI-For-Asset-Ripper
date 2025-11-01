# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'browseWindowgUtAof.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(680, 466)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 26pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit_search_bundles = QLineEdit(self.tab)
        self.lineEdit_search_bundles.setObjectName(u"lineEdit_search_bundles")

        self.verticalLayout.addWidget(self.lineEdit_search_bundles)

        self.treeWidget = QTreeWidget(self.tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 26pt \"Microsoft YaHei UI\";")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_bundleLink = QPushButton(self.tab_2)
        self.pushButton_bundleLink.setObjectName(u"pushButton_bundleLink")

        self.horizontalLayout.addWidget(self.pushButton_bundleLink)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(self.tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -123, 624, 518))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 500))
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")

        self.verticalLayout_5.addWidget(self.label_4)

        self.lineEdit_search_collection_assets = QLineEdit(self.widget)
        self.lineEdit_search_collection_assets.setObjectName(u"lineEdit_search_collection_assets")

        self.verticalLayout_5.addWidget(self.lineEdit_search_collection_assets)

        self.tableWidget_assets = QTableWidget(self.widget)
        self.tableWidget_assets.setObjectName(u"tableWidget_assets")

        self.verticalLayout_5.addWidget(self.tableWidget_assets)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")

        self.verticalLayout_5.addWidget(self.label_5)

        self.lineEdit_search_collection_dep = QLineEdit(self.widget)
        self.lineEdit_search_collection_dep.setObjectName(u"lineEdit_search_collection_dep")

        self.verticalLayout_5.addWidget(self.lineEdit_search_collection_dep)

        self.tableWidget_dependencies = QTableWidget(self.widget)
        self.tableWidget_dependencies.setObjectName(u"tableWidget_dependencies")

        self.verticalLayout_5.addWidget(self.tableWidget_dependencies)


        self.verticalLayout_4.addWidget(self.widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_6 = QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_resources_title = QLabel(self.tab_3)
        self.label_resources_title.setObjectName(u"label_resources_title")
        self.label_resources_title.setStyleSheet(u"font: 26pt \"Microsoft YaHei UI\";")

        self.verticalLayout_6.addWidget(self.label_resources_title)

        self.label_7 = QLabel(self.tab_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")

        self.verticalLayout_6.addWidget(self.label_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_res_bundle = QPushButton(self.tab_3)
        self.pushButton_res_bundle.setObjectName(u"pushButton_res_bundle")

        self.horizontalLayout_2.addWidget(self.pushButton_res_bundle)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.label_8 = QLabel(self.tab_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")

        self.verticalLayout_6.addWidget(self.label_8)

        self.label_size = QLabel(self.tab_3)
        self.label_size.setObjectName(u"label_size")

        self.verticalLayout_6.addWidget(self.label_size)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.pushButton_saveres = QPushButton(self.tab_3)
        self.pushButton_saveres.setObjectName(u"pushButton_saveres")

        self.horizontalLayout_3.addWidget(self.pushButton_saveres)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Loaded Files", None))
        self.label.setText("")
        self.lineEdit_search_bundles.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Bundles", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"No Items Opened", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Bundle", None))
        self.pushButton_bundleLink.setText(QCoreApplication.translate("Dialog", u"No Items Opened", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Assets", None))
        self.lineEdit_search_collection_assets.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search...", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Dependencies", None))
        self.lineEdit_search_collection_dep.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Collections", None))
        self.label_resources_title.setText(QCoreApplication.translate("Dialog", u"No Items Opened", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Bundle", None))
        self.pushButton_res_bundle.setText(QCoreApplication.translate("Dialog", u"No Items Opened", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Size", None))
        self.label_size.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.pushButton_saveres.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Resources", None))
    # retranslateUi

