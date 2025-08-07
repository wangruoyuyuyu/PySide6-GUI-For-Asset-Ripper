from uip import ui_exportAllWindow
from PySide6 import QtWidgets
import path_saver, os, exportingWindow, api


class ExportAllWindow(ui_exportAllWindow.Ui_Dialog, QtWidgets.QDialog):
    SAFE_QSS = """QPushButton{
    padding-left:21px;
    padding-right:21px;
    padding-top:10.5px;
    padding-bottom:10.5px;
	background-color: rgb(13, 110, 253);
	color: rgb(255, 255, 255);
}
QPushButton:hover{
	background-color: rgb(11, 94, 215);
}
QPushButton:disabled{
	color: rgb(175, 177, 180);
	background-color: rgb(43, 86, 180);
}"""
    DANGER_QSS = """QPushButton{
    padding-left:21px;
    padding-right:21px;
    padding-top:10.5px;
    padding-bottom:10.5px;
	background-color: rgb(220, 53, 69);
	color: rgb(255, 255, 255);
}
QPushButton:hover{
	background-color: rgb(187, 45, 59);
}"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.exporting_window = None

        self.connectSignals()

    def connectSignals(self):
        self.pushButton_sel_dir.clicked.connect(self.select_dir)
        self.lineEdit.textChanged.connect(self.checkDangerAndEnabled)
        self.checkBox_create_subdir.checkStateChanged.connect(
            self.checkDangerAndEnabled
        )
        self.pushButton_export_project.clicked.connect(self.export_unity_project)

    def export_unity_project(self):
        self.exporting_window = exportingWindow.ExportingWindow(self)
        self.exporting_window.setModal(True)
        self.exporting_window.show()
        api.export_unity_project(
            self.lineEdit.text(),
            self.checkBox_create_subdir.isChecked(),
            self.parent().port,
        )

    def export_primary_content(self):
        self.exporting_window = exportingWindow.ExportingWindow(self)
        self.exporting_window.setModal(True)
        self.exporting_window.show()
        api._export_primary_content(
            self.lineEdit.text(),
            self.checkBox_create_subdir.isChecked(),
            self.parent().port,
        )

    def select_dir(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory...", dir=path_saver.get_last_export_path()
        )
        if not dir_path:
            return  # 取消了
        path_saver.save_last_export_path(dir_path)
        self.lineEdit.setText(dir_path)

    def checkDangerAndEnabled(self):
        if self.isButtonsEnabled():
            self.pushButton_export_prim_content.setEnabled(True)
            self.pushButton_export_project.setEnabled(True)
        else:
            self.pushButton_export_prim_content.setStyleSheet(self.SAFE_QSS)
            self.pushButton_export_prim_content.setEnabled(False)
            self.pushButton_export_project.setStyleSheet(self.SAFE_QSS)
            self.pushButton_export_project.setEnabled(False)
            self.label_danger.setStyleSheet("color:rgba(255,255,255,0)")
            return
        if self.isDanger():
            self.pushButton_export_prim_content.setStyleSheet(self.DANGER_QSS)
            self.pushButton_export_project.setStyleSheet(self.DANGER_QSS)
            self.label_danger.setStyleSheet("color:black")
        else:
            self.pushButton_export_prim_content.setStyleSheet(self.SAFE_QSS)
            self.pushButton_export_project.setStyleSheet(self.SAFE_QSS)
            self.label_danger.setStyleSheet("color:rgba(255,255,255,0)")

    def isDanger(self) -> bool:
        isEmpty = not len(os.listdir(self.lineEdit.text()))
        if not isEmpty:
            if self.checkBox_create_subdir.isChecked():
                return False
            return not isEmpty
        return False

    def isButtonsEnabled(self) -> bool:
        if "C:" == self.lineEdit.text().strip("/").strip("\\"):
            return False
        return os.path.isdir(self.lineEdit.text())


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    eaw = ExportAllWindow()
    eaw.show()
    qa.exec()
