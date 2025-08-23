from uip import ui_browseWindow
from PySide6 import QtWidgets, QtCore, QtGui
import api, _thread, pyperclip, assetWindow, downloader, typing


class BrowseWindow(QtWidgets.QDialog, ui_browseWindow.Ui_Dialog):
    class Types(object):
        BUNDLE = 0
        COLLECTION = 1

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.type = None
        self._data = None
        self.collections = None
        self._res = None
        self.downloaders: typing.List[downloader.Downloader] = list()

        self.setupEvent()

    def setupEvent(self):
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.rightClicked)
        self.treeWidget.doubleClicked.connect(self.doubleClicked)

    def doubleClicked(self):
        if not self.get_item_level(self.treeWidget.selectedItems()[0]):
            return
        self.open_content()

    def rightClicked(self):
        if not self.get_item_level(self.treeWidget.selectedItems()[0]):
            self.contextMenuFirstLevel()
        else:
            self.contextMenuSecondLevel()

    def contextMenuFirstLevel(self):
        menu = QtWidgets.QMenu()
        action1 = menu.addAction("&Export All")
        action2 = menu.addAction(
            "E&xpand"
            if not self.treeWidget.selectedItems()[0].isExpanded()
            else "&Collapse"
        )
        action1.triggered.connect(self.parent().to_export_all)
        action2.triggered.connect(self.expand_selection)
        menu.exec(QtGui.QCursor.pos())

    def contextMenuSecondLevel(self):
        menu = QtWidgets.QMenu()
        action1 = menu.addAction("&Open")
        action2 = menu.addAction("&Export All")
        action1.triggered.connect(self.open_content)
        action2.triggered.connect(self.parent().to_export_all)
        menu.exec(QtGui.QCursor.pos())

    def expand_selection(self):
        self.treeWidget.selectedItems()[0].setExpanded(
            not self.treeWidget.selectedItems()[0].isExpanded()
        )

    def open_content(self, *args, from_collections=False, from_link=False, link=""):
        self.update()
        QtWidgets.QApplication.processEvents()
        if from_link and link:
            url = link
        elif not from_collections:
            parent_text = self.treeWidget.selectedItems()[0].parent().text(0)
            text = self.treeWidget.selectedItems()[0].text(0)
            url = self._data[parent_text][text]
        else:
            url = list(self.collections["Bundle"].values())[0]
        print(url)
        if "Collections" in url:
            self.tabWidget.setCurrentIndex(1)
        elif "Resources" in url:
            self.tabWidget.setCurrentIndex(2)
        else:
            self.tabWidget.setCurrentIndex(0)
        if not ("Collections" in url or "Resources" in url):
            self.is_data_loaded = False
            self.loaded_data = None
            self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
            self._prompt_window.setWindowTitle("加载中... Loading...")
            self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self._prompt_window.show()
            self.setEnabled(False)
            _thread.start_new_thread(self._open_content, (url,))
            while not self.is_data_loaded:
                self.update()
                QtWidgets.QApplication.processEvents()
            self.setData(self.loaded_data)
            self.setEnabled(True)
            self._prompt_window.close()
        elif "Resources" in url:
            self.is_data_loaded = False
            self.loaded_data = None
            self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
            self._prompt_window.setWindowTitle("加载中... Loading...")
            self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self._prompt_window.show()
            self.setEnabled(False)
            _thread.start_new_thread(self._open_resources, (url,))
            while not self.is_data_loaded:
                self.update()
                QtWidgets.QApplication.processEvents()
            self._prompt_window.close()
            self.setEnabled(True)
            self.setResources(self.loaded_data)
        else:
            self.is_data_loaded = False
            self.loaded_data = None
            self._prompt_window = QtWidgets.QLabel("请稍后... Please wait...")
            self._prompt_window.setWindowTitle("加载中... Loading...")
            self._prompt_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self._prompt_window.show()
            self.setEnabled(False)
            _thread.start_new_thread(self._open_collections, (url,))
            while not self.is_data_loaded:
                self.update()
                QtWidgets.QApplication.processEvents()
            self._prompt_window.close()
            self.setEnabled(True)
            self.setCollections(self.loaded_data)

    def _open_resources(self, url):
        self.loaded_data = api.get_loaded_resources(
            self.parent().port, from_url=True, url=url
        )
        print(self.loaded_data)
        self.is_data_loaded = True

    def setResources(self, data: dict):
        self._res = data
        self.label_resources_title.setText(data["h1"])
        self.pushButton_res_bundle.setText(list(data["bundle"].keys())[0])
        self.label_size.setText(data["size"])
        self.pushButton_res_bundle.clicked.connect(self.open_back_res_bundle)
        self.pushButton_saveres.clicked.connect(self.save_res)

    def open_back_res_bundle(self):
        if not self._res:
            return  # 没有
        self.open_content(from_link=True, link=list(self._res["bundle"].values())[0])

    def save_res(self):
        if not self._res:
            return
        save_name: str = list(self._res["save"].keys())[0]
        filters = f"{save_name.split(".")[1]} File (*.{save_name.split(".")[1]})"
        save_path = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File...", filter=filters, dir=save_name
        )[0]
        if not save_path:
            return  # 取消了
        self.downloaders.append(downloader.Downloader(self))
        full_link = f"http://localhost:{self.parent().port}{list(self._res["save"].values())[0]}"
        self.downloaders[-1].show()
        self.downloaders[-1].file_download(full_link, save_path)

    def _open_collections(self, url):
        self.loaded_data = api.get_loaded_collections(
            self.parent().port, from_url=True, url=url
        )
        self.is_data_loaded = True

    def get_item_level(self, item: QtWidgets.QTreeWidgetItem):
        """
        获取指定项的层级
        :param item: QTreeWidgetItem对象
        :return: 项的层级，从0开始计数（根节点为0层）
        """
        level = 0
        parent = item.parent()
        while parent:
            level += 1
            parent = parent.parent()
        return level

    def _open_content(self, url):
        data = api.get_loaded_files(self.parent().port, from_url=True, url=url)
        self.loaded_data = data
        self.is_data_loaded = True

    def setType(self, type_):
        self.type = type_

    def open_back_bundles(self):
        self.open_content(from_collections=True)

    def setData(self, data: dict):
        # print(data)
        self.treeWidget.clear()
        self.treeWidget.setHeaderLabel("items")
        tvs = list()
        for k, v in data.items():
            qte = QtWidgets.QTreeWidgetItem([k])
            if type(v) != dict:
                continue
            for l in v.keys():
                c = QtWidgets.QTreeWidgetItem([l])
                qte.addChild(c)
            tvs += [qte]
        self.treeWidget.insertTopLevelItems(0, tvs)
        self.treeWidget.expandAll()
        if data["H1"]:
            self.label.setText(data["H1"])
        self._data = data

    def setCollections(self, data: dict):
        self.tableWidget_assets.clear()
        self.tableWidget_dependencies.clear()
        if "H1" in data.keys():
            if data["H1"]:
                self.label_2.setText(data["H1"])
        if "Bundle" in data.keys():
            if data["Bundle"]:
                self.pushButton_bundleLink.setText(list(data["Bundle"].keys())[0])
                self.pushButton_bundleLink.clicked.connect(self.open_back_bundles)
        self.setupTable(data, "Assets", self.tableWidget_assets)
        self.setupTable(data, "Dependencies", self.tableWidget_dependencies)
        self.collections = data

    def setupTable(self, data: dict, key: str, widget: QtWidgets.QTableWidget):
        widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.connectTableEvents(widget)
        if key in data.keys():
            if data[key]:
                assets_data: list = data[key]
                widget.setColumnCount(len(assets_data))
                if assets_data[0]:
                    widget.setRowCount(len(assets_data[0]) - 1)
                vlabel = list()
                index = 0
                for i in assets_data:
                    for j in range(len(i)):
                        if not j:
                            vlabel.append(i[j])
                            continue
                        item = QtWidgets.QTableWidgetItem(i[j])
                        widget.setItem(j - 1, index, item)
                    index += 1
                widget.setHorizontalHeaderLabels(vlabel)
                widget.horizontalHeader().setSectionResizeMode(
                    QtWidgets.QHeaderView.Stretch
                )
            else:
                widget.clear()
                widget.setRowCount(0)
                widget.setColumnCount(0)
        else:
            widget.clear()
            widget.setRowCount(0)
            widget.setColumnCount(0)

    def connectTableEvents(self, table: QtWidgets.QTableWidget):
        table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 关键修复：保留信号传递的pos参数，并通过lambda参数绑定当前table
        table.customContextMenuRequested.connect(
            lambda pos, t=table: self.customTableMenu(t, pos)
        )
        table.doubleClicked.connect(lambda: self.open_asset(table))

    def customTableMenu(self, table, pos):  # 新增pos参数（位置）
        menu = QtWidgets.QMenu()
        action1 = menu.addAction("&Copy")
        action2 = menu.addAction("&Open")
        action1.triggered.connect(lambda: self.copy_table_value(table))
        action2.triggered.connect(lambda: self.open_asset(table))
        # 可选：使用pos在点击位置显示菜单（更符合直觉）
        menu.exec(QtGui.QCursor.pos())

    def copy_table_value(self, table: QtWidgets.QTableWidget):
        s = str()
        for i in table.selectedItems():
            s += i.text() + " "
        pyperclip.copy(s)

    def open_asset(self, table: QtWidgets.QTableWidget):
        name = table.objectName().split("_")[1]
        if name == "dependencies":
            link_list = self.collections["Dependencies_links"]
        elif name == "assets":
            link_list = self.collections["Assets_links"]
        link = link_list[table.selectedItems()[0].row()]
        print("openedLink:" + link)
        if "Collections" in link:
            self.open_content(from_link=True, link=link)
        elif "Assets" in link:
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
            self.assetWindow = assetWindow.AssetWindow(self)
            self.assetWindow.show()
            self.assetWindow.setData(self.loaded_data)

    def _open_assets(self, link):
        self.loaded_data = api.get_loaded_assets(
            self.parent().port, from_url=True, url=link
        )
        # print(self.loaded_data)
        self.is_data_loaded = True


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    bw = BrowseWindow()
    bw.show()
    qa.exec()
