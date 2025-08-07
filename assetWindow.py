from uip import ui_assetWindow
from PySide6 import QtWidgets, QtCore, QtGui
import _thread, api, browseWindow, pyperclip, downloader, typing, os, path_saver


class AssetWindow(ui_assetWindow.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self._data = None
        self.video_check_interval = None
        self.text_json = None
        self.text_yaml = None
        self.text = None
        self.text_set = False
        self.html_code = self.js_code = None
        self.has_font = False
        self.text_json_set = False
        self.text_yaml_set = False
        self.is_font_loaded = False

        self.vdo_name_got = False
        self.vdo_name = None

        self.loaded_data = None
        self.is_data_loaded = False  # 修复拼写错误
        self.saving_dialogs: typing.List[downloader.Downloader] = list()

        # 视频进度进度条交互相关变量
        self.is_dragging = False  # 是否是否是否是否正在被拖动
        self.video_total_ms = 0  # 视频总时长（毫秒）

        winflags = self.windowFlags()
        winflags |= QtCore.Qt.WindowMinimizeButtonHint
        self.setWindowFlags(winflags)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_text)
        self.timer.start(500)

        # 初始化进度条交互
        self.init_progress_bar()

    def init_progress_bar(self):
        """初始化进度条交互功能"""
        # 设置进度条范围
        self.horizontalSlider_playprogress.setRange(0, 100)

        # 连接滑块信号
        self.horizontalSlider_playprogress.sliderPressed.connect(self.on_slider_pressed)
        self.horizontalSlider_playprogress.sliderReleased.connect(
            self.on_slider_released
        )
        self.horizontalSlider_playprogress.valueChanged.connect(
            self.on_slider_value_changed
        )

    def on_slider_pressed(self):
        """进度条开始拖动时调用"""
        self.is_dragging = True
        # 暂停自动更新，避免冲突
        if self.video_check_interval:
            self.video_check_interval.stop()

    def on_slider_released(self):
        """
        结束拖动时调用
        计算并设置视频新位置
        """
        self.is_dragging = False

        # 恢复进度百分比计算目标位置（毫秒）
        if self.video_total_ms > 0:
            target_percent = self.horizontalSlider_playprogress.value() / 100.0
            target_ms = int(target_percent * self.video_total_ms)
            # 设置视频位置
            self.widget_video_play.setPlayProgress(target_ms)

        # 恢复自动更新
        if self.video_check_interval and not self.video_check_interval.isActive():
            self.video_check_interval.start()

    def on_slider_value_changed(self, value):
        """进度条拖动过程中更新        仅在拖动状态下更新显示，不实际修改视频位置"""
        if self.is_dragging and self.video_total_ms > 0:
            # 计算当前拖动位置对应的时间并显示
            current_ms = int(value / 100.0 * self.video_total_ms)
            allseconds = current_ms / 1000
            hours = int(allseconds / 3600)
            mins = int(allseconds / 60) % 60
            secs = int(allseconds % 60)
            fstr = self._check_time_format(f"{hours}:{mins}:{secs}")
            self.label_playprogress.setText(fstr)

    def update_vdo_proc(self):
        """更新视频进度（仅在非拖动状态下）"""
        # 拖动中不更新进度条，避免冲突
        if self.is_dragging:
            return

        proc = self.widget_video_play.getPlayProgress()
        current_ms, total_ms = proc[0], proc[1]

        # 更新总时长记录
        self.video_total_ms = total_ms

        if not total_ms:  # 视频未加载完成
            self.label_playprogress.setText("--:--:--")
            self.horizontalSlider_playprogress.setValue(0)
            return

        # 计算进度百分比
        perc = (current_ms / total_ms) * 100 if total_ms > 0 else 0
        self.horizontalSlider_playprogress.setValue(int(perc))

        # 更新时间显示
        allseconds = current_ms / 1000
        hours = int(allseconds / 3600)
        mins = int(allseconds / 60) % 60
        secs = int(allseconds % 60)
        fstr = f"{hours}:{mins}:{secs}"
        fstr = self._check_time_format(fstr)
        self.label_playprogress.setText(fstr)

    # 以下为原代码其他方法（保持不变）
    def check_text(self):
        if self.text_json and not self.text_json_set:
            self.textEdit_json.setText(self.text_json)
            self.textEdit_json.setReadOnly(True)
            self.text_json_set = True
        if self.text_yaml and not self.text_yaml_set:
            self.textEdit_yaml.setText(self.text_yaml)
            self.textEdit_yaml.setReadOnly(True)
            self.text_yaml_set = True
        if self.text and not self.text_set:
            self.textEdit.setText(self.text)
            self.textEdit.setReadOnly(True)
            self.text_set = True
        if (
            self.has_font
            and self.html_code
            and self.js_code
            and not self.is_font_loaded
        ):
            self.webEngineView_fontpreview.setHtml(self.html_code)
            self.webEngineView_fontpreview.loadFinished.connect(
                self._on_font_page_loaded
            )
            self.is_font_loaded = True

    def _on_font_page_loaded(self, success):
        if success:
            self.webEngineView_fontpreview.page().runJavaScript(
                self.js_code, self._on_font_js_executed
            )
        else:
            print("字体预览页面加载失败")

    def _on_font_js_executed(self, result):
        print("JS执行完成，结果:", result)

    def setData(self, data: dict):
        if "H1" in data.keys():
            if data["H1"]:
                self.label_title.setText(data["H1"])
        self.setupTable(data, "Information", self.tableWidget_info)
        self.setupTable(data, "Dependencies", self.tableWidget_dependencies)
        self.setupTable(data, "Development", self.tableWidget_development)
        self.setupTableEvents()
        if data["Image"]:
            if len(data["Image"].values()) > 0:
                self.tabWidget.setTabEnabled(2, True)
                url: str = list(data["Image"].values())[0]
                if url.startswith("/"):
                    url = f"http://localhost:{self.parent().parent().port}" + url
                self.widget_image.loader.load_image(url)
            else:
                self.tabWidget.setTabEnabled(2, False)
        else:
            self.tabWidget.setTabEnabled(2, False)
        if data["Video"]:
            self.tabWidget.setTabEnabled(6, True)
            full_link = f"http://localhost:{self.parent().parent().port}{data['Video']}"
            self.widget_video_play.load_video(full_link)
            self.video_check_interval = QtCore.QTimer()
            self.video_check_interval.timeout.connect(self.update_vdo_proc)
            self.video_check_interval.start(1000)  # 1秒更新一次
            self.pushButton_savevdo.clicked.connect(self.save_vdo)
        else:
            self.pushButton_savevdo.clicked.connect(self.empty)
            if self.video_check_interval:
                self.video_check_interval.stop()
            self.tabWidget.setTabEnabled(6, False)
        if data["Model"]:
            self.tabWidget.setTabEnabled(3, True)
            full_link = f"http://localhost:{self.parent().parent().port}{data['Model']}"
            self.widget_modelpreview.load_from_url(full_link)
        else:
            self.tabWidget.setTabEnabled(3, False)
        if data["Audio"]:
            self.pushButton_save_audio.clicked.connect(self.save_audio)
            self.tabWidget.setTabEnabled(1, True)
            full_link = f"http://localhost:{self.parent().parent().port}{data['Audio']}"
            self.widget_audioplay.load_audio(full_link)
        else:
            self.pushButton_save_audio.clicked.connect(self.empty)
            self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(
            5, bool(data["Font"]) if "Font" in data.keys() else False
        )
        if data["Text"]:
            self.pushButton_save_text.clicked.connect(self.save_text)
            self.tabWidget.setTabEnabled(4, True)
        else:
            self.pushButton_save_text.clicked.connect(self.empty)
            self.tabWidget.setTabEnabled(4, False)
        if data["Json"]:
            self.pushButton_save_json.clicked.connect(self.save_json)
        else:
            self.pushButton_save_json.clicked.connect(self.empty)
        if data["Yaml"]:
            self.pushButton_save_yaml.clicked.connect(self.save_yaml)
        else:
            self.pushButton_save_yaml.connect(self.empty)
        self._data = data
        _thread.start_new_thread(self._load_text, tuple())
        self.tabWidget.setCurrentIndex(0)

    def empty(self):
        pass

    def save_audio(self):
        self.audio_name = None
        self.audio_name_got = None
        self.setEnabled(False)
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self._prompt_window.show()
        _thread.start_new_thread(self._get_audio_name, tuple())
        while not self.audio_name_got:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)

        save_name: str = self.audio_name
        filters = f"{save_name.split(".")[1]} File (*.{save_name.split(".")[1]})"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File...",
            dir=os.path.join(path_saver.get_last_export_path(), save_name),
            filter=filters,
        )[0]
        if not save_path:
            return
        path_saver.save_last_export_path(path_saver.get_file_dir(save_path))
        self.saving_dialogs.append(downloader.Downloader(self))
        self.saving_dialogs[-1].show()
        full_url = (
            f"http://localhost:{self.parent().parent().port}{self._data["Audio"]}"
        )
        self.saving_dialogs[-1].file_download(full_url, save_path)

    def _get_audio_name(self):
        self.audio_name = api.get_audio_name(
            self._data["Audio"], self.parent().parent().port, self.label_title.text()
        )
        self.audio_name_got = True

    def save_vdo(self):
        self.vdo_name = None
        self.vdo_name_got = False
        self.setEnabled(False)
        self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
        self._prompt_window.setWindowTitle("加载中... Loading...")
        self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self._prompt_window.show()
        _thread.start_new_thread(self._get_file_name, tuple())
        while not self.vdo_name_got:
            self.update()
            QtWidgets.QApplication.processEvents()
        self._prompt_window.close()
        self.setEnabled(True)

        save_name: str = self.vdo_name
        filters = f"{save_name.split(".")[1]} File (*.{save_name.split(".")[1]})"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File...",
            dir=os.path.join(path_saver.get_last_export_path(), save_name),
            filter=filters,
        )[0]
        if not save_path:
            return
        path_saver.save_last_export_path(path_saver.get_file_dir(save_path))
        self.saving_dialogs.append(downloader.Downloader(self))
        self.saving_dialogs[-1].show()
        full_url = (
            f"http://localhost:{self.parent().parent().port}{self._data["Video"]}"
        )
        self.saving_dialogs[-1].file_download(full_url, save_path)

    def _get_file_name(self):
        self.vdo_name = api.get_video_name(
            self._data["Video"], self.parent().parent().port
        )
        self.vdo_name_got = True

    def save_yaml(self):
        if not self._data["Yaml"]:
            return
        save_name: str = list(self._data["Yaml"].keys())[0]
        filters = f"Asset File (*.asset);;Yaml File (*.yaml);;Text File (*.txt);;All Files (*.*)"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File...",
            dir=os.path.join(path_saver.get_last_export_path(), save_name),
            filter=filters,
        )[0]
        if not save_path:
            return
        path_saver.save_last_export_path(path_saver.get_file_dir(save_path))
        self.saving_dialogs.append(downloader.Downloader(self))
        self.saving_dialogs[-1].show()
        full_url = f"http://localhost:{self.parent().parent().port}{list(self._data["Yaml"].values())[0]}"
        self.saving_dialogs[-1].file_download(full_url, save_path)

    def save_json(self):
        if not self._data["Json"]:
            return
        save_name: str = list(self._data["Json"].keys())[0]
        filters = f"Json File (*.json);;Text File (*.txt);;All Files (*.*)"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File...",
            dir=os.path.join(path_saver.get_last_export_path(), save_name),
            filter=filters,
        )[0]
        if not save_path:
            return
        path_saver.save_last_export_path(path_saver.get_file_dir(save_path))
        self.saving_dialogs.append(downloader.Downloader(self))
        self.saving_dialogs[-1].show()
        full_url = f"http://localhost:{self.parent().parent().port}{list(self._data["Json"].values())[0]}"
        self.saving_dialogs[-1].file_download(full_url, save_path)

    def save_text(self):
        if not self._data["Text"]:
            return  # 没有
        save_name: str = list(self._data["Text"].keys())[0]
        filters = f"{save_name.split(".")[1]} File (*.{save_name.split(".")[1]});;Text File (*.txt);;All Files(*.*)"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File...",
            dir=os.path.join(path_saver.get_last_export_path(), save_name),
            filter=filters,
        )[0]
        if not save_path:
            return  # 取消了
        path_saver.save_last_export_path(path_saver.get_file_dir(save_path))
        self.saving_dialogs.append(downloader.Downloader(self))
        full_url = f"http://localhost:{self.parent().parent().port}{list(self._data["Text"].values())[0]}"
        self.saving_dialogs[-1].show()
        self.saving_dialogs[-1].file_download(full_url, save_path)

    def _check_time_format(self, fstr: str):
        h, m, s = fstr.split(":")
        return f"{h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}"

    def _load_text(self):
        if self._data["Yaml"] and len(self._data["Yaml"].values()) > 0:
            text = api.get_loaded_text(
                self.parent().parent().port,
                from_url=True,
                url=list(self._data["Yaml"].values())[0],
            )
            self.text_yaml = text
        if self._data["Json"] and len(self._data["Json"].values()) > 0:
            text = api.get_loaded_text(
                self.parent().parent().port,
                from_url=True,
                url=list(self._data["Json"].values())[0],
            )
            self.text_json = text
        if self._data["Text"]:
            if len(self._data["Text"].values()) > 0:
                text = api.get_loaded_text(
                    self.parent().parent().port,
                    from_url=True,
                    url=list(self._data["Text"].values())[0],
                )
                self.text = text
        if self._data["Font"]:
            file_name = api.get_loaded_font_name(
                self._data["Font"], self.parent().parent().port
            )
            if file_name:
                file_name_without_ext = file_name.split(".")[0]
                self.has_font = True
                self.html_code = f"""<h1 style="font-family: {file_name_without_ext}">Preview Font (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)</h1>"""
                self.js_code = (
                    f"""const fontFace = new FontFace('{file_name_without_ext}', 'url(http://localhost:{self.parent().parent().port}{self._data["Font"]})');"""
                    + """
document.fonts.add(fontFace);
fontFace.load().then().catch(function(error) {{
  console.error('Font loading failed: ${error}');
}});"""
                )
        else:
            self.tabWidget.setTabEnabled(5, False)

    def get_widget_tab_index(
        self, target_widget, tab_widget: QtWidgets.QTabWidget = None
    ) -> int:
        if tab_widget is None:
            tab_widget = self.tabWidget
        for i in range(tab_widget.count()):
            tab_page = tab_widget.widget(i)
            if tab_page.isAncestorOf(target_widget):
                return i
        return -1

    def setupTable(self, data: dict, key: str, widget: QtWidgets.QTableWidget):
        widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        if key in data.keys() and data[key]:
            assets_data: list = data[key]
            widget.setColumnCount(len(assets_data) - 1)
            if assets_data[0]:
                widget.setRowCount(len(assets_data[0]))
            hlabel = list()
            index = 0
            for i in assets_data:
                for j in range(len(i)):
                    if not index:
                        hlabel.append(i[j])
                        continue
                    item = QtWidgets.QTableWidgetItem(i[j])
                    widget.setItem(j, index - 1, item)
                index += 1
            widget.setVerticalHeaderLabels(hlabel)
            widget.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch
            )
        else:
            widget.clear()
            widget.setRowCount(0)
            widget.setColumnCount(0)

    def setupTableEvents(self):
        self.tableWidget_info.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_info.customContextMenuRequested.connect(self.info_context_menu)
        self.tableWidget_info.doubleClicked.connect(
            lambda: self.open_content(self.tableWidget_info, "Information")
        )
        self.tableWidget_dependencies.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_dependencies.customContextMenuRequested.connect(
            self.dependencies_context_menu
        )
        self.tableWidget_dependencies.doubleClicked.connect(
            lambda: self.open_content(self.tableWidget_dependencies, "Dependencies")
        )
        self.tableWidget_development.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_development.customContextMenuRequested.connect(
            self.development_context_menu
        )

    def development_context_menu(self):
        menu = QtWidgets.QMenu()
        action = menu.addAction("Copy")
        action.triggered.connect(self.copy_development_value)
        menu.exec(QtGui.QCursor.pos())

    def copy_development_value(self):
        text = self.tableWidget_development.selectedItems()[0].text()
        pyperclip.copy(text)

    def info_context_menu(self):
        menu = QtWidgets.QMenu()
        action1 = menu.addAction("Open")
        if "Information_links" in self._data.keys():
            if self._data["Information_links"][
                self.tableWidget_info.selectedItems()[0].row()
            ]:
                action1.setEnabled(True)
            else:
                action1.setEnabled(False)
        else:
            action1.setEnabled(False)
        action2 = menu.addAction("Copy")
        action1.triggered.connect(
            lambda: self.open_content(self.tableWidget_info, "Information")
        )
        action2.triggered.connect(lambda: self.copy_table_value(self.tableWidget_info))
        menu.exec(QtGui.QCursor.pos())

    def dependencies_context_menu(self):
        menu = QtWidgets.QMenu()
        action1 = menu.addAction("Open")
        if "Dependencies_links" in self._data.keys():
            if self._data["Dependencies_links"][
                self.tableWidget_dependencies.selectedItems()[0].row()
            ]:
                action1.setEnabled(True)
            else:
                action1.setEnabled(False)
        else:
            action1.setEnabled(False)
        action2 = menu.addAction("Copy")
        action1.triggered.connect(
            lambda: self.open_content(self.tableWidget_dependencies, "Dependencies")
        )
        action2.triggered.connect(
            lambda: self.copy_table_value(self.tableWidget_dependencies)
        )
        menu.exec(QtGui.QCursor.pos())

    def open_content(self, table: QtWidgets.QTableWidget, selection_text: str):
        link = self._data[f"{selection_text}_links"][table.selectedItems()[0].row()]
        if "Assets" in link:
            self.is_data_loaded = False
            self.loaded_data = None
            self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
            self._prompt_window.setWindowTitle("加载中... Loading...")
            self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self._prompt_window.show()
            self.setEnabled(False)
            _thread.start_new_thread(self._open_assets, (link,))
            while not self.is_data_loaded:
                self.update()
                QtWidgets.QApplication.processEvents()
            self._prompt_window.close()
            self.setEnabled(True)
            self.setData(self.loaded_data)

        else:
            self.showMinimized()
            parent: browseWindow.BrowseWindow = self.parent()
            parent.open_content(from_link=True, link=link)

    def copy_table_value(self, table: QtWidgets.QTableWidget):
        s = str()
        for i in table.selectedItems():
            s += i.text() + " "
        pyperclip.copy(s.strip())

    def _open_assets(self, link):
        self.loaded_data = api.get_loaded_assets(
            self.parent().parent().port, from_url=True, url=link
        )
        # print(self.loaded_data)
        self.is_data_loaded = True

    def closeEvent(self, arg__1):
        try:
            self.widget_video_play.stop()
        except Exception:
            pass
        return super().closeEvent(arg__1)


if __name__ == "__main__":
    qa = QtWidgets.QApplication([])
    aw = AssetWindow()
    aw.show()
    qa.exec()
