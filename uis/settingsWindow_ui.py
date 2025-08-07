# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWindow.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(648, 484)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 26pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.label)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 622, 879))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 1, 1, 1)

        self.comboBox_bund_ass_em = QComboBox(self.groupBox)
        self.comboBox_bund_ass_em.addItem("")
        self.comboBox_bund_ass_em.addItem("")
        self.comboBox_bund_ass_em.addItem("")
        self.comboBox_bund_ass_em.setObjectName(u"comboBox_bund_ass_em")

        self.gridLayout_2.addWidget(self.comboBox_bund_ass_em, 5, 0, 1, 1)

        self.checkBox_rm_null_attr = QCheckBox(self.groupBox)
        self.checkBox_rm_null_attr.setObjectName(u"checkBox_rm_null_attr")

        self.gridLayout_2.addWidget(self.checkBox_rm_null_attr, 1, 0, 1, 1)

        self.checkBox_skp_opt_fold = QCheckBox(self.groupBox)
        self.checkBox_skp_opt_fold.setObjectName(u"checkBox_skp_opt_fold")

        self.gridLayout_2.addWidget(self.checkBox_skp_opt_fold, 0, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label_6, 6, 1, 1, 1)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 7, 0, 1, 2)

        self.checkBox_pub_asm = QCheckBox(self.groupBox)
        self.checkBox_pub_asm.setObjectName(u"checkBox_pub_asm")

        self.gridLayout_2.addWidget(self.checkBox_pub_asm, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 10, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 8, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEdit_def_ver = QLineEdit(self.groupBox)
        self.lineEdit_def_ver.setObjectName(u"lineEdit_def_ver")

        self.gridLayout_2.addWidget(self.lineEdit_def_ver, 3, 0, 1, 2)

        self.comboBox_scr_cont_lev = QComboBox(self.groupBox)
        self.comboBox_scr_cont_lev.addItem("")
        self.comboBox_scr_cont_lev.addItem("")
        self.comboBox_scr_cont_lev.addItem("")
        self.comboBox_scr_cont_lev.addItem("")
        self.comboBox_scr_cont_lev.setObjectName(u"comboBox_scr_cont_lev")

        self.gridLayout_2.addWidget(self.comboBox_scr_cont_lev, 5, 1, 1, 1)

        self.checkBox_enable_pref_ol = QCheckBox(self.groupBox)
        self.checkBox_enable_pref_ol.setObjectName(u"checkBox_enable_pref_ol")

        self.gridLayout_2.addWidget(self.checkBox_enable_pref_ol, 9, 0, 1, 1)

        self.lineEdit_targ_ver_chang = QLineEdit(self.groupBox)
        self.lineEdit_targ_ver_chang.setObjectName(u"lineEdit_targ_ver_chang")

        self.gridLayout_2.addWidget(self.lineEdit_targ_ver_chang, 11, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_23 = QLabel(self.groupBox_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_23, 8, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_2)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_3.addWidget(self.label_21, 6, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_24, 8, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_13, 2, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_19, 5, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_3.addWidget(self.label_22, 6, 1, 1, 1)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_18, 5, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_16, 3, 1, 1, 1)

        self.comboBox_shd_form_exp = QComboBox(self.groupBox_2)
        self.comboBox_shd_form_exp.addItem("")
        self.comboBox_shd_form_exp.addItem("")
        self.comboBox_shd_form_exp.addItem("")
        self.comboBox_shd_form_exp.addItem("")
        self.comboBox_shd_form_exp.setObjectName(u"comboBox_shd_form_exp")

        self.gridLayout_3.addWidget(self.comboBox_shd_form_exp, 4, 1, 1, 1)

        self.comboBox_lang_ver = QComboBox(self.groupBox_2)
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.addItem("")
        self.comboBox_lang_ver.setObjectName(u"comboBox_lang_ver")

        self.gridLayout_3.addWidget(self.comboBox_lang_ver, 7, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_12, 2, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_3.addWidget(self.label_15, 3, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_20, 5, 2, 1, 1)

        self.comboBox_sprite_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_sprite_exp_form.addItem("")
        self.comboBox_sprite_exp_form.addItem("")
        self.comboBox_sprite_exp_form.addItem("")
        self.comboBox_sprite_exp_form.setObjectName(u"comboBox_sprite_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_sprite_exp_form, 4, 0, 1, 1)

        self.comboBox_ta_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_ta_exp_form.addItem("")
        self.comboBox_ta_exp_form.addItem("")
        self.comboBox_ta_exp_form.addItem("")
        self.comboBox_ta_exp_form.setObjectName(u"comboBox_ta_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_ta_exp_form, 4, 2, 1, 1)

        self.comboBox_i_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.addItem("")
        self.comboBox_i_exp_form.setObjectName(u"comboBox_i_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_i_exp_form, 1, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_14, 2, 2, 1, 1)

        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_17, 3, 2, 1, 1)

        self.comboBox_lm_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_lm_exp_form.addItem("")
        self.comboBox_lm_exp_form.addItem("")
        self.comboBox_lm_exp_form.addItem("")
        self.comboBox_lm_exp_form.setObjectName(u"comboBox_lm_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_lm_exp_form, 1, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 0, 1, 1, 1)

        self.comboBox_ado_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_ado_exp_form.addItem("")
        self.comboBox_ado_exp_form.addItem("")
        self.comboBox_ado_exp_form.addItem("")
        self.comboBox_ado_exp_form.addItem("")
        self.comboBox_ado_exp_form.setObjectName(u"comboBox_ado_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_ado_exp_form, 1, 0, 1, 1)

        self.comboBox_scr_exp_form = QComboBox(self.groupBox_2)
        self.comboBox_scr_exp_form.addItem("")
        self.comboBox_scr_exp_form.addItem("")
        self.comboBox_scr_exp_form.addItem("")
        self.comboBox_scr_exp_form.addItem("")
        self.comboBox_scr_exp_form.setObjectName(u"comboBox_scr_exp_form")

        self.gridLayout_3.addWidget(self.comboBox_scr_exp_form, 7, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBox_script_fully_qua_name = QCheckBox(self.groupBox_2)
        self.checkBox_script_fully_qua_name.setObjectName(u"checkBox_script_fully_qua_name")

        self.gridLayout_4.addWidget(self.checkBox_script_fully_qua_name, 0, 0, 1, 1)

        self.label_script_use_full_qua_name = QLabel(self.groupBox_2)
        self.label_script_use_full_qua_name.setObjectName(u"label_script_use_full_qua_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_script_use_full_qua_name.sizePolicy().hasHeightForWidth())
        self.label_script_use_full_qua_name.setSizePolicy(sizePolicy)
        self.label_script_use_full_qua_name.setWordWrap(True)

        self.gridLayout_4.addWidget(self.label_script_use_full_qua_name, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 9, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.checkBox_save_disk = QCheckBox(self.groupBox_2)
        self.checkBox_save_disk.setObjectName(u"checkBox_save_disk")

        self.gridLayout_5.addWidget(self.checkBox_save_disk, 0, 0, 1, 1)

        self.label_save_disk = QLabel(self.groupBox_2)
        self.label_save_disk.setObjectName(u"label_save_disk")
        sizePolicy.setHeightForWidth(self.label_save_disk.sizePolicy().hasHeightForWidth())
        self.label_save_disk.setSizePolicy(sizePolicy)
        self.label_save_disk.setWordWrap(True)

        self.gridLayout_5.addWidget(self.label_save_disk, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 9, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.comboBox_bund_ass_em.setCurrentIndex(2)
        self.comboBox_scr_cont_lev.setCurrentIndex(2)
        self.comboBox_shd_form_exp.setCurrentIndex(0)
        self.comboBox_lang_ver.setCurrentIndex(17)
        self.comboBox_sprite_exp_form.setCurrentIndex(0)
        self.comboBox_ta_exp_form.setCurrentIndex(2)
        self.comboBox_i_exp_form.setCurrentIndex(4)
        self.comboBox_lm_exp_form.setCurrentIndex(2)
        self.comboBox_ado_exp_form.setCurrentIndex(2)
        self.comboBox_scr_exp_form.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Asset Ripper Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Configuration Options", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Import", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Script Content Level", None))
        self.comboBox_bund_ass_em.setItemText(0, QCoreApplication.translate("Dialog", u"Group By Asset Type", None))
        self.comboBox_bund_ass_em.setItemText(1, QCoreApplication.translate("Dialog", u"Group By Bundle Name", None))
        self.comboBox_bund_ass_em.setItemText(2, QCoreApplication.translate("Dialog", u"Direct Export", None))

        self.comboBox_bund_ass_em.setCurrentText(QCoreApplication.translate("Dialog", u"Direct Export", None))
        self.checkBox_rm_null_attr.setText(QCoreApplication.translate("Dialog", u"Remove Nullable Attributes", None))
        self.checkBox_skp_opt_fold.setText(QCoreApplication.translate("Dialog", u"Skip StreamingAssets Folder", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Default. This exports full methods for Mono games and dummy methods for IL2Cpp games.", None))
        self.checkBox_pub_asm.setText(QCoreApplication.translate("Dialog", u"Publicize Assemblies", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Bundled assets are exported without grouping.</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Target Version For Version Changing", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Experimental", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Bundled Assets Export Mode", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Default Version", None))
        self.comboBox_scr_cont_lev.setItemText(0, QCoreApplication.translate("Dialog", u"Level 0", None))
        self.comboBox_scr_cont_lev.setItemText(1, QCoreApplication.translate("Dialog", u"Level 1", None))
        self.comboBox_scr_cont_lev.setItemText(2, QCoreApplication.translate("Dialog", u"Level 2", None))
        self.comboBox_scr_cont_lev.setItemText(3, QCoreApplication.translate("Dialog", u"Level 3", None))

        self.checkBox_enable_pref_ol.setText(QCoreApplication.translate("Dialog", u"Enable Prefab Outlining", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Export", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"The C# language version to be used when decompiling scripts.\n"
"\n"
"", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"C# Language Version", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Special assemblies like Assembly-CSharp are decompiled. Other assemblies are exported in their compiled Dll form.\n"
"\n"
"", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"This affects all exported images.", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Export the shader as a dummy shader. Although it preserves data like the properties and fallback, it uses general, opaque shader code.", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Lightmap Texture Export Format", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Script Export Format", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Export as yaml assets which can be viewed in the editor. This is the only mode that ensures a precise recovery of all metadata of sprites.", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Audio Export Format", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Shader Export Format", None))
        self.comboBox_shd_form_exp.setItemText(0, QCoreApplication.translate("Dialog", u"Dummy Shader", None))
        self.comboBox_shd_form_exp.setItemText(1, QCoreApplication.translate("Dialog", u"Yaml Asset", None))
        self.comboBox_shd_form_exp.setItemText(2, QCoreApplication.translate("Dialog", u"Disassembly", None))
        self.comboBox_shd_form_exp.setItemText(3, QCoreApplication.translate("Dialog", u"Decompilation", None))

        self.comboBox_lang_ver.setItemText(0, QCoreApplication.translate("Dialog", u"C# 1", None))
        self.comboBox_lang_ver.setItemText(1, QCoreApplication.translate("Dialog", u"C# 2", None))
        self.comboBox_lang_ver.setItemText(2, QCoreApplication.translate("Dialog", u"C# 3", None))
        self.comboBox_lang_ver.setItemText(3, QCoreApplication.translate("Dialog", u"C# 4", None))
        self.comboBox_lang_ver.setItemText(4, QCoreApplication.translate("Dialog", u"C# 5", None))
        self.comboBox_lang_ver.setItemText(5, QCoreApplication.translate("Dialog", u"C# 6", None))
        self.comboBox_lang_ver.setItemText(6, QCoreApplication.translate("Dialog", u"C# 7", None))
        self.comboBox_lang_ver.setItemText(7, QCoreApplication.translate("Dialog", u"C# 7.1", None))
        self.comboBox_lang_ver.setItemText(8, QCoreApplication.translate("Dialog", u"C# 7.2", None))
        self.comboBox_lang_ver.setItemText(9, QCoreApplication.translate("Dialog", u"C# 7.3", None))
        self.comboBox_lang_ver.setItemText(10, QCoreApplication.translate("Dialog", u"C# 8", None))
        self.comboBox_lang_ver.setItemText(11, QCoreApplication.translate("Dialog", u"C# 9", None))
        self.comboBox_lang_ver.setItemText(12, QCoreApplication.translate("Dialog", u"C# 10", None))
        self.comboBox_lang_ver.setItemText(13, QCoreApplication.translate("Dialog", u"C# 11", None))
        self.comboBox_lang_ver.setItemText(14, QCoreApplication.translate("Dialog", u"C# 12", None))
        self.comboBox_lang_ver.setItemText(15, QCoreApplication.translate("Dialog", u"C# Latest", None))
        self.comboBox_lang_ver.setItemText(16, QCoreApplication.translate("Dialog", u"Automatic - Experimental", None))
        self.comboBox_lang_ver.setItemText(17, QCoreApplication.translate("Dialog", u"Automatic - Safe", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Export assets as the content type embedded inside the FSB. Most audio types are exported as WAV, some are exported as OGG.", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Sprite Export Format", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Export as a plain text file, but try to guess the correct file extension (e.g. JSON files get the .json extension).", None))
        self.comboBox_sprite_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Yaml", None))
        self.comboBox_sprite_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Unity", None))
        self.comboBox_sprite_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Texture", None))

        self.comboBox_ta_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Bytes", None))
        self.comboBox_ta_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Plain Text", None))
        self.comboBox_ta_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Parse", None))

        self.comboBox_i_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Bmp", None))
        self.comboBox_i_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Exr", None))
        self.comboBox_i_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Hdr", None))
        self.comboBox_i_exp_form.setItemText(3, QCoreApplication.translate("Dialog", u"Jpeg", None))
        self.comboBox_i_exp_form.setItemText(4, QCoreApplication.translate("Dialog", u"Png", None))
        self.comboBox_i_exp_form.setItemText(5, QCoreApplication.translate("Dialog", u"Tga", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"This affects all exported lightmap textures.", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"TextAsset Export Format", None))
        self.comboBox_lm_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Exr", None))
        self.comboBox_lm_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Image", None))
        self.comboBox_lm_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Yaml", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Image Export Format", None))
        self.comboBox_ado_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Yaml", None))
        self.comboBox_ado_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Raw", None))
        self.comboBox_ado_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Default", None))
        self.comboBox_ado_exp_form.setItemText(3, QCoreApplication.translate("Dialog", u"Convert to WAV", None))

        self.comboBox_scr_exp_form.setItemText(0, QCoreApplication.translate("Dialog", u"Decompilation", None))
        self.comboBox_scr_exp_form.setItemText(1, QCoreApplication.translate("Dialog", u"Hybrid", None))
        self.comboBox_scr_exp_form.setItemText(2, QCoreApplication.translate("Dialog", u"Dll Export With Renaming", None))
        self.comboBox_scr_exp_form.setItemText(3, QCoreApplication.translate("Dialog", u"Dll Export Without Renaming", None))

        self.checkBox_script_fully_qua_name.setText("")
        self.label_script_use_full_qua_name.setText(QCoreApplication.translate("Dialog", u"Scripts use fully-qualified type names\n"
"", None))
        self.checkBox_save_disk.setText("")
        self.label_save_disk.setText(QCoreApplication.translate("Dialog", u"Save Settings to Disk", None))
    # retranslateUi

