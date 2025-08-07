from uip import ui_cmdWindow
from PySide6 import QtWidgets
import os.path, api, path_saver


class CmdWindow(ui_cmdWindow.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.connectSignals()

    def connectSignals(self):
        self.pushButton_sel_file.clicked.connect(self.sel_file)
        self.pushButton_sel_folder.clicked.connect(self.sel_folder)
        self.lineEdit.textChanged.connect(self.check_existing)

    def check_existing(self):
        if os.path.exists(self.lineEdit.text()):
            self.buttonBox_open.setEnabled(True)
        else:
            self.buttonBox_open.setEnabled(False)

    def sel_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File...", dir=path_saver.get_last_path()
        )[0]
        if file:
            path_saver.save_last_path(path_saver.get_file_dir(file))
            self.lineEdit.setText(file)

    def sel_folder(self):
        file = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory...", dir=path_saver.get_last_path()
        )
        if file:
            path_saver.save_last_path(file)
            self.lineEdit.setText(file)

    def accept(self):
        api.load_file_or_folder_from_path(self.lineEdit.text(), self.parent().port)
        return super().accept()


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    cw = CmdWindow()
    cw.show()
    qa.exec()
