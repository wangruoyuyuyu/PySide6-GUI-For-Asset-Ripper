from uip import ui_exportingWindow
from PySide6 import QtWidgets
import os


class ExportingWindow(ui_exportingWindow.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.progressBar.setRange(0, 100)

    def setValue(self, now: int, all: int, text: str):
        if now != None:
            self.label_exported_num.setText(str(now))
        if all != None:
            self.label_allNum.setText(str(all))
        if now != None and all != None:
            percent = now / all * 100
            self.progressBar.setValue(int(percent))
        self.label_fileName.setText(text)
        if text == "Finished Exporting":
            self.buttonBox.buttons()[0].setText("OK")
            os.system(
                f'explorer.exe /Select,"{self.parent().lineEdit.text()}"'
            )  # 打开文件夹

    def stop(self):
        is_ok = (
            QtWidgets.QMessageBox.question(
                self,
                "Cancel Exporting",
                "Cancelling Exporting is not supported in Asset Ripper.You need to restart the application after cancelling,are you sure?",
            )
            == 16384
        )
        if is_ok and self.parent():
            self.close()
            self.parent().close()
            self.parent().parent().close()
        return is_ok

    def reject(self):
        if self.label_fileName.text() == "Finished Exporting":
            return super().reject()
        if not self.stop():
            return False
        return super().reject()


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    ew = ExportingWindow()
    ew.show()
    qa.exec()
