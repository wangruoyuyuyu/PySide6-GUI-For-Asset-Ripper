from uip import ui_settingsWindow
from PySide6 import QtWidgets, QtCore
import _thread, api, constants
from iniConfig import IniFile


class WheelFilter(QtCore.QObject):
    def __init__(self, scrollarea: QtWidgets.QScrollArea = None):
        super().__init__()
        self.scrollarea = scrollarea

    def eventFilter(self, watched, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Type.Wheel:
            if self.scrollarea:
                self.scrollarea.wheelEvent(event)
            return True  # 跳过
        return super().eventFilter(watched, event)


class SettingsWindow(ui_settingsWindow.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.form_names: dict = None

        self.init_local_config()

        self.setEventFilter()
        self.setupSignal()
        self.retranslateBtnBx()

    def retranslateBtnBx(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText(
            QtCore.QCoreApplication.translate("Dialog", "Cancel")
        )
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save).setText(
            QtCore.QCoreApplication.translate("Dialog", "Save")
        )
        print(QtCore.QCoreApplication.translate("Dialog", "Save"))

    def setFormNames(self, fn: dict):
        self.form_names = fn

    def setupSignal(self):
        self.label_script_use_full_qua_name.mouseReleaseEvent = self.label_event_1
        self.label_save_disk.mouseReleaseEvent = self.label_event_2

    def label_event_1(self, event: QtCore.QEvent):
        self.checkBox_script_fully_qua_name.click()

    def label_event_2(self, event: QtCore.QEvent):
        self.checkBox_save_disk.click()

    def setEventFilter(self):
        self.efs = list()
        for i in self.all_combo_boxes:
            self.efs.append(WheelFilter(self.scrollArea))
            i.installEventFilter(self.efs[-1])

    @property
    def all_combo_boxes(self):
        return [
            self.comboBox_ado_exp_form,
            self.comboBox_bund_ass_em,
            self.comboBox_i_exp_form,
            self.comboBox_lm_exp_form,
            self.comboBox_lang_ver,
            self.comboBox_scr_cont_lev,
            self.comboBox_scr_exp_form,
            self.comboBox_shd_form_exp,
            self.comboBox_sprite_exp_form,
            self.comboBox_ta_exp_form,
        ]

    @property
    def inversed_settings_mapping(self):
        return dict(map(reversed, self.settings_mapping.items()))

    @property
    def settings_mapping(self):
        return {
            "Bundled Assets Export Mode": self.comboBox_bund_ass_em,
            "Script Content Level": self.comboBox_scr_cont_lev,
            "Audio Export Format": self.comboBox_ado_exp_form,
            "Image Export Format": self.comboBox_i_exp_form,
            "Lightmap Texture Export Format": self.comboBox_lm_exp_form,
            "Sprite Export Format": self.comboBox_sprite_exp_form,
            "Shader Export Format": self.comboBox_shd_form_exp,
            "TextAsset Export Format": self.comboBox_ta_exp_form,
            "C# Language Version": self.comboBox_lang_ver,
            "Script Export Format": self.comboBox_scr_exp_form,
            "Default Version": self.lineEdit_def_ver,
            "Target Version For Version Changing": self.lineEdit_targ_ver_chang,
            "Skip StreamingAssets Folder": self.checkBox_skp_opt_fold,
            "Remove Nullable Attributes": self.checkBox_rm_null_attr,
            "Publicize Assemblies": self.checkBox_pub_asm,
            "Enable Prefab Outlining": self.checkBox_enable_pref_ol,
            "Scripts use fully-qualified type names": self.checkBox_script_fully_qua_name,
            "Save Settings to Disk": self.checkBox_save_disk,
        }

    @property
    def all_widgets(self):
        return self.settings_mapping.values()

    def setData(self, data: dict):
        for i in data.keys():
            if not i in self.settings_mapping.keys():
                continue  # 付费版功能，咱没有
            wid = self.settings_mapping[i]
            if type(wid) == QtWidgets.QCheckBox:
                wid.setChecked(data[i])
            elif type(wid) == QtWidgets.QComboBox:
                wid.setCurrentIndex(data[i])
            elif type(wid) == QtWidgets.QLineEdit:
                wid.setText(data[i])

    def _get_post_values(self) -> dict:
        ret = dict()
        for i in self.all_widgets:
            if type(i) == QtWidgets.QComboBox:
                form_name = self.form_names[self.inversed_settings_mapping[i]]
                selection = self.form_names[form_name + "_options"][i.currentIndex()]
                ret[form_name] = selection
            elif type(i) == QtWidgets.QCheckBox:
                if not i.isChecked():
                    continue  # 没选不需要提交
                form_name = self.form_names[self.inversed_settings_mapping[i]]
                ret[form_name] = "on"
            elif type(i) == QtWidgets.QLineEdit:
                form_name = self.form_names[self.inversed_settings_mapping[i]]
                ret[form_name] = i.text()
        return ret

    def accept(self):
        self.save_local_config()

        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.post_ret_code = None
        self.posted = False
        _thread.start_new_thread(self._post_settings, tuple())
        while not self.posted:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)
        if self.post_ret_code == 200 or self.post_ret_code == 302:
            QtWidgets.QMessageBox.information(
                self,
                QtCore.QCoreApplication.translate("Dialog", "Success"),
                QtCore.QCoreApplication.translate("Dialog", "Settings Saved"),
            )
        else:
            QtWidgets.QMessageBox.critical(
                self,
                QtCore.QCoreApplication.translate("Dialog", "Failed"),
                QtCore.QCoreApplication.translate(
                    "Dialog", "Cannot Save Settings, status code:"
                )
                + str(self.post_ret_code),
            )
            return False
        return super().accept()

    def _post_settings(self):
        self.post_ret_code = api.post_settings(
            self._get_post_values(), self.parent().port
        )
        self.posted = True

    def init_local_config(self):
        self.ini_config = IniFile(constants.CONFIG_FILE_NAME)
        isTaskBarProg = self.ini_config.getValue("GUI", "show_taskbar_progress", 1)
        if isTaskBarProg != "0" and isTaskBarProg != 0:
            self.checkBox_show_taskbar_prog.setChecked(True)
        else:
            self.checkBox_show_taskbar_prog.setChecked(False)

    def save_local_config(self):
        self.ini_config.setValue(
            "GUI",
            "show_taskbar_progress",
            int(self.checkBox_show_taskbar_prog.isChecked()),
        )
        with open(constants.CONFIG_FILE_NAME, "w+") as f:
            self.ini_config.writeToFile(f)
            f.close()


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    sw = SettingsWindow()
    sw.show()
    qa.exec()
