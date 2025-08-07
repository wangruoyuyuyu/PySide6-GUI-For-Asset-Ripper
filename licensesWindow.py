from uip import ui_licenseWindow
from PySide6 import QtWidgets


class LicencesWindow(ui_licenseWindow.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.listWidget.setCurrentRow(0)
        self.connectSignals()
        if self.parent():
            self.webEngineView.setUrl(f"http://localhost:{self.parent().port}/Licenses")

    def connectSignals(self):
        self.listWidget.itemSelectionChanged.connect(self.change_index)

    def change_index(self):
        self.stackedWidget.setCurrentIndex(self.listWidget.currentRow())


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    lw = LicencesWindow()
    lw.show()
    qa.exec()
