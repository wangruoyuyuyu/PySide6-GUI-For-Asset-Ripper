from PySide6 import QtCore, QtWidgets
import PyTaskbar


class TaskbarProgManager(QtCore.QObject, PyTaskbar.Progress):
    class States:
        from PyTaskbar import NORMAL, ERROR, LOADING, WARNING

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        PyTaskbar.Progress.__init__(self, self.parent().winId())

        self._value = 0
        self._maximumValue = 100
        self._state = self.States.NORMAL

    def value(self) -> int:
        return self._value

    def setValue(self, value: int):
        self._value = value
        self.set_progress(value, self._maximumValue)

    def setMaximumValue(self, value: int):
        self._maximumValue = value

    def maximumValue(self) -> int:
        return self._maximumValue

    def state(self) -> int:
        return self._state

    def setState(self, state: int):
        self._state = state
        self.set_progress_type(state)


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    mw = QtWidgets.QMainWindow()
    mw.show()
    print(mw.winId())
    interval = QtCore.QTimer()
    tpm = TaskbarProgManager(mw)

    def set_():
        tpm.setState(TaskbarProgManager.States.LOADING)
        tpm.setValue(50)

    interval.timeout.connect(set_)
    interval.start(1000)
    qa.exec()
