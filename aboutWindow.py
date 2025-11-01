from uip import ui_aboutWindow
from PySide6 import QtWidgets
import webbrowser


class AboutWindow(ui_aboutWindow.Ui_Dialog, QtWidgets.QDialog):
    VERSION = "1.1.0"

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.label_version.setText(self.VERSION)
        self.setupSignals()

    def setupSignals(self):
        self.pushButton.clicked.connect(
            lambda: webbrowser.open(
                "https://github.com/wangruoyuyuyu/PySide6-GUI-For-Asset-Ripper"
            )
        )


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    aw = AboutWindow()
    aw.show()
    qa.exec()
