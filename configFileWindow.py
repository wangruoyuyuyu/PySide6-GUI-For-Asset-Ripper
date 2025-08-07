from PySide6 import QtWidgets, QtCore
from uip import ui_configFileWindow, ui_configNoneWindow, ui_configSettingsFrame
import api, _thread, time, win32gui, windowGetter, win32con


class ConfigNoneFrame(ui_configNoneWindow.Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class ConfigSettingsFrame(ui_configSettingsFrame.Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class ConfigFileWindow(QtWidgets.QDialog, ui_configFileWindow.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self._data = None
        self.need_refresh = False
        self.need_close_win_1 = None

        self.pages = {}
        # 确保标签页初始就有布局
        for i in range(self.tabWidget_2.count()):
            tab_page = self.tabWidget_2.widget(i)
            if not tab_page.layout():
                layout = QtWidgets.QVBoxLayout(tab_page)
                layout.setContentsMargins(0, 0, 0, 0)

        api.StatusMachine.onReplaceFileFinished = self.onReplaceFileFinished
        self.refresh_check_interval = QtCore.QTimer()
        self.refresh_check_interval.timeout.connect(self.check_refresh)
        self.refresh_check_interval.start()

    def check_refresh(self):
        if self.need_refresh:
            self.need_refresh = False
            self.refresh_configs()

    def onReplaceFileFinished(self, res: api.requests.Response):
        if not (self.need_close_win_1 or (self.need_close_win_1 is None)):
            self.need_close_win_1 = True
        if res.status_code == 200 or res.status_code == 302:
            self.need_refresh = True
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "Cannot replace config file, status code:" + str(res.status_code),
            )

    def setData(self, data: dict):
        # 彻底清理旧部件（修复断开连接的错误）
        for page in self.pages.values():
            # 从布局中移除
            if page.parent():
                layout = page.parent().layout()
                if layout:
                    layout.removeWidget(page)

            # 正确断开所有信号连接的方式
            # 方法1：使用blockSignals临时阻断信号（推荐）
            page.blockSignals(True)

            # 方法2：如果确实需要彻底断开，可以遍历所有信号（复杂场景用）
            # if hasattr(page, 'pushButton'):
            #     page.pushButton.clicked.disconnect()
            # if hasattr(page, 'pushButton_replace'):
            #     page.pushButton_replace.clicked.disconnect()
            # if hasattr(page, 'pushButton_remove'):
            #     page.pushButton_remove.clicked.disconnect()

            # 将父对象设为None，彻底脱离标签页
            page.setParent(None)
            # 销毁部件（推荐，彻底释放资源）
            page.deleteLater()

        self.pages.clear()

        # 遍历数据创建新页面
        for key, value in data.items():
            tab_index = self.tab_indexes.get(key)
            if tab_index is None:
                continue

            tab_page = self.tabWidget_2.widget(tab_index)
            if not tab_page:
                continue

            # 创建对应页面部件
            if len(value) == 1:
                page = ConfigNoneFrame(tab_page)
                page.pushButton.clicked.connect(self.replace_config)
            elif len(value) == 2:
                page = ConfigSettingsFrame(tab_page)
                page.textEdit.setText(value[0])
                page.pushButton_replace.clicked.connect(self.replace_config)
                page.pushButton_remove.clicked.connect(self.remove_config)
            else:
                continue

            # 添加到布局
            layout = tab_page.layout()
            if layout:
                layout.addWidget(page)
                self.pages[key] = page

        self._data = data

    # 其余方法保持不变...
    def replace_config(self):
        if not self._data:
            return
        name_list = self._data[list(self.config_keys)[self.tabWidget_2.currentIndex()]]
        length = len(
            self._data[list(self.config_keys)[self.tabWidget_2.currentIndex()]]
        )
        if not length:
            return
        if length == 1:
            name = name_list[0]
        elif length == 2:
            name = name_list[1]
        api.replace_config_file(name, self.parent().port)
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.need_close_win = False
        _thread.start_new_thread(self._wait_window, tuple())
        while not self.need_close_win:
            QtWidgets.QApplication.processEvents()
            self.update()
        time.sleep(1)
        self._prompt_window.close()

    def remove_config(self):
        if not self._data:
            return
        name_list = self._data[list(self.config_keys)[self.tabWidget_2.currentIndex()]]
        length = len(
            self._data[list(self.config_keys)[self.tabWidget_2.currentIndex()]]
        )
        if not length:
            return
        if length == 1:
            name = name_list[0]
        elif length == 2:
            name = name_list[1]
        api.remove_config_file(name, self.parent().port)
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.need_close_win_1 = False
        while not self.need_close_win_1:
            QtWidgets.QApplication.processEvents()
            self.update()
        time.sleep(1)
        self._prompt_window.close()
        self.need_close_win_1 = None

    def _wait_window(self):
        while True:
            pid = (
                windowGetter.find_process_by_name("AssetRipper.GUI.Free.exe")
                if not windowGetter.StatusMachine.known_pid
                else windowGetter.StatusMachine.known_pid
            )
            windows = windowGetter.get_window_info(pid)
            if len(windows) < 1:
                continue
            hwnd = windows[0]["hwnd"]
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print("foreground set")
            self.setEnabled(True)
            self.need_close_win = True
            break

    @property
    def tab_indexes(self):
        return {
            "ImportSettings": 0,
            "ProcessingSettings": 1,
            "ExportSettings": 2,
            "EngineResourceData": 3,
        }

    @property
    def config_keys(self):
        return self.tab_indexes.keys()

    def refresh_configs(self):
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.configs = None
        self.configs_got = False
        _thread.start_new_thread(self._get_config, tuple())
        while not self.configs_got:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)
        self.setData(self.configs)

    def _get_config(self):
        self.configs = api.get_configs(self.parent().port)
        print(self.configs)
        self.configs_got = True


if __name__ == "__main__":
    qa = QtWidgets.QApplication([])
    cfw = ConfigFileWindow()
    cfw.show()
    qa.exec()
