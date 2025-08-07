from PySide6 import QtWidgets, QtCore, QtGui
import webbrowser, api, browseWindow, settingsWindow, configFileWindow, cmdWindow, exportAllWindow, licensesWindow, aboutWindow
from uip import ui_mainWindow
import windowGetter, win32gui, win32con, _thread, time, os, path_saver


class PathOpenMethod(object):
    FAST = 0
    LEGACY = 1


class MainWindow(ui_mainWindow.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        self.port = None
        self.hasFile = False
        self.version = None
        self.version_option = None
        self.export_all_window = None
        super().__init__()
        self.setupUi(self)

        if os.path.exists("./icon.ico"):
            icon = QtGui.QIcon("./icon.ico")
            self.setWindowIcon(icon)

        self.setupLinks()
        self.setupActions()
        api.StatusMachine.onApiCallFinished = self.onApiCallFinished

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_btn_stat)
        self.timer.start(500)

    def check_btn_stat(self):
        if self.hasFile:
            self.pushButton.setEnabled(True)
            self.actionExport_All_Files.setEnabled(True)
            self.pushButton.setStyleSheet(
                "QPushButton{background-color:#198754;color:white;}QPushButton:hover{background-color:#157347}"
            )
            self.pushButton.setText("View Loaded Files")
        else:
            self.pushButton.setEnabled(False)
            self.actionExport_All_Files.setEnabled(False)
            self.pushButton.setStyleSheet(str())
            self.pushButton.setText("No Files Loaded")
        if self.version:
            if not self.version_option:
                self.version_option = QtGui.QAction(list(self.version.keys())[0])
                self.version_option.triggered.connect(self.open_version)
                self.menu_Export.addAction(self.version_option)
        else:
            if self.version_option:
                self.menu_Export.removeAction(self.version_option)
                self.version_option = None

    def open_version(self):
        webbrowser.open(list(self.version.values())[0])

    def onApiCallFinished(self, res: api.requests.Response):
        print("返回码：", res.status_code)
        if res.status_code == 302 or res.status_code == 200:
            self.hasFile = api.check_is_file(self.port)
            print("hasFile:", self.hasFile)
            self.version = api.check_version(self.port)
            print("Unity version:", self.version)

    def export_all(self):
        pass

    def set_port(self, port):
        self.port = port

    def setupActions(self):
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionReset.triggered.connect(self.reset)

        self.actionSettings.triggered.connect(self.to_settings)
        self.actionSettings_2.triggered.connect(self.to_settings)
        self.actionConfiguration_Files.triggered.connect(self.to_config_files)
        self.actionCommands.triggered.connect(self.to_cmds)
        self.actionExport_All_Files.triggered.connect(self.to_export_all)
        self.actionPrivacy.triggered.connect(self.privacy_dialog)
        self.actionLicenses.triggered.connect(self.to_licenses)

        self.actionOpenAPI_JSON.triggered.connect(
            lambda: webbrowser.open(f"http://localhost:{self.port}/openapi.json")
        )
        self.actionSwagger_Documentation.triggered.connect(
            lambda: webbrowser.open(f"http://localhost:{self.port}/swagger/")
        )
        self.actionOriginal_UI.triggered.connect(
            lambda: webbrowser.open(f"http://localhost:{self.port}/")
        )

        self.actionAbout_Qt.triggered.connect(
            lambda: QtWidgets.QMessageBox.aboutQt(self)
        )
        self.action_About.triggered.connect(self.about)

        self.pushButton.clicked.connect(self.view_files)

    def about(self):
        self.about_window = aboutWindow.AboutWindow(self)
        self.about_window.show()

    def to_licenses(self):
        self.lic_window = licensesWindow.LicencesWindow(self)
        self.lic_window.show()

    def privacy_dialog(self):
        QtWidgets.QMessageBox.information(
            self, "Privacy", "This application doesn't access the Internet."
        )

    def to_cmds(self):
        if self.hasFile:
            self.to_export_all()
        else:
            self.cmds_window = cmdWindow.CmdWindow(self)
            self.cmds_window.setModal(True)
            self.cmds_window.show()

    def to_export_all(self):
        self.export_all_window = exportAllWindow.ExportAllWindow(self)
        self.export_all_window.setModal(True)
        self.export_all_window.show()

    def to_config_files(self):
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

        self.config_dialog = configFileWindow.ConfigFileWindow(self)
        self.config_dialog.setModal(True)
        self.config_dialog.show()
        self.config_dialog.setData(self.configs)

    def _get_config(self):
        self.configs = api.get_configs(self.port)
        print(self.configs)
        self.configs_got = True

    def to_settings(self):
        if self.hasFile:
            QtWidgets.QMessageBox.information(
                self,
                "Configuration Options",
                "Settings can only be changed before loading files.",
            )
        else:
            self.open_settings()

    def open_settings(self):
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.settings = None
        self.settings_names = None
        self.settings_got = False
        _thread.start_new_thread(self._get_settings, tuple())
        while not self.settings_got:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)

        self.settings_window = settingsWindow.SettingsWindow(self)
        self.settings_window.setModal(True)
        flags = self.settings_window.windowFlags()
        flags |= QtCore.Qt.WindowType.WindowMaximizeButtonHint
        self.settings_window.setWindowFlags(flags)
        self.settings_window.show()
        self.settings_window.setData(self.settings)
        self.settings_window.setFormNames(self.settings_names)

    def _get_settings(self):
        ret = api.get_settings(self.port)
        self.settings = ret[0]
        self.settings_names = ret[1]
        self.settings_got = True
        print(self.settings)

    def view_files(self, *d):
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        self.data = None
        self.finished = False
        _thread.start_new_thread(self._view_files, tuple())
        while not self.finished:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)
        self.browseFileDialog = browseWindow.BrowseWindow(self)
        self.browseFileDialog.setModal(True)
        self.browseFileDialog.show()
        self.browseFileDialog.setType(browseWindow.BrowseWindow.Types.BUNDLE)
        self.browseFileDialog.setData(self.data)

    def _view_files(self, *d):
        self.data = api.get_loaded_files(self.port)
        self.finished = True

    def reset(self, *d):
        api.reset(self.port)
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.show()
        self.setEnabled(False)
        timer = QtCore.QElapsedTimer()
        timer.start()
        while timer.elapsed() <= 1000:
            QtWidgets.QApplication.processEvents()
            self.update()
        self._prompt_window.close()
        self.setEnabled(True)

    def open_file(self, *d, method=PathOpenMethod.FAST):
        if method == PathOpenMethod.LEGACY:
            api.open_file(self.port)
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
        elif method == PathOpenMethod.FAST:
            path = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select File...", dir=path_saver.get_last_path()
            )[0]
            if not path:
                return  # 取消了
            path_saver.save_last_path(path_saver.get_file_dir(path))
            api.load_file_or_folder_from_path(path, port=self.port)

    def open_folder(self, *d, method=PathOpenMethod.FAST):
        if method == PathOpenMethod.LEGACY:
            api.open_folder(self.port)
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
        elif method == PathOpenMethod.FAST:
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory...", dir=path_saver.get_last_path()
            )
            if not path:
                return  # 取消了
            path_saver.save_last_path(path)
            api.load_file_or_folder_from_path(path, port=self.port)

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

    def setupLinks(self):
        dic = {
            self.linkBtn1: "https://patreon.com/ds5678",
            self.linkBtn2: "https://paypal.me/ds5678",
            self.linkBtn3: "https://github.com/sponsors/ds5678",
            self.linkBtn4: "ar://dialog1",
            self.linkBtn5: "ar://lics",
        }
        for button, url in dic.items():
            if url.startswith("http"):
                # 使用默认参数创建局部变量
                button.clicked.connect(
                    lambda checked=False, link=url: webbrowser.open(link)
                )

    def finishExportingEvent(self):
        if self.export_all_window:
            if self.export_all_window.exporting_window:
                self.export_all_window.exporting_window.setValue(
                    None, None, "Finished Exporting"
                )

    def handleExportingOutPut(self, current: str, total: str, name: str):
        if self.export_all_window:
            if self.export_all_window.exporting_window:
                try:
                    self.export_all_window.exporting_window.setValue(
                        int(current.strip()), int(total.strip()), name
                    )
                except TypeError:
                    pass

    def handleDecompilingMessage(self, name: str):
        if self.export_all_window:
            if self.export_all_window.exporting_window:
                self.export_all_window.exporting_window.setValue(
                    None, None, f"Decompiling: {name}"
                )

    def handleSavingMessage(self, content: str):
        if self.export_all_window:
            if self.export_all_window.exporting_window:
                self.export_all_window.exporting_window.setValue(
                    None, None, f"Saving: {content}"
                )

    def setProcessPid(self, pid: int):
        windowGetter.StatusMachine.known_pid = pid


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    mw = MainWindow()
    mw.show()
    qa.exec()
