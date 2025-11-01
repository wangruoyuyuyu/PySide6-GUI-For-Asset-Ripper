from PySide6 import QtCore, QtWidgets
from INSLogger import Logger


class TreeSearcher(QtCore.QObject):
    logger = Logger("Searcher")

    def __init__(self, search_bar: QtWidgets.QLineEdit):
        super().__init__(parent=search_bar)
        self._orig_dic = dict()
        self._treeWidget = None
        self._last_text = str()
        self._last_dict = None

        self.parent().textChanged.connect(self.search)

    def search(self):
        txt = self.parent().text()
        # self.logger.debug(self._last_text,self._last_dict)
        if self._last_text in txt and self._last_dict:
            data = self.searchedDict(self._last_dict, txt)
            self.setData(data)
            self._last_dict = data
            self.logger.log("finished fast search")
        else:
            data = self.searchedDict(self._orig_dic, txt)
            self.setData(data)
            self._last_dict = data
            self.logger.log("finished normal search")
        self._last_text = txt

    @staticmethod
    def searchedDict(orig: dict, text: str) -> dict:
        out = dict()
        for k, v in orig.items():
            if not type(v) == dict:
                continue
            out[k] = dict()
            for i, j in v.items():
                if text in i:
                    out[k][i] = j
        return out

    def origDict(self) -> dict:
        return self._orig_dic

    def setOrigDict(self, dic: dict):
        self._orig_dic = dic

    def __bool__(self):
        return bool(self._orig_dic) and bool()

    def treeWidget(self) -> QtWidgets.QTreeWidget:
        return self._treeWidget

    def setTreeWidget(self, widget: QtWidgets.QTreeWidget):
        self._treeWidget = widget

    def setData(self, data: dict):
        # self.logger.log(data)
        self._treeWidget.clear()
        self._treeWidget.setHeaderLabel("items")
        tvs = list()
        for k, v in data.items():
            trans = QtCore.QCoreApplication.translate("Dialog", k)
            qte = QtWidgets.QTreeWidgetItem([trans])
            if type(v) != dict:
                continue
            for l in v.keys():
                c = QtWidgets.QTreeWidgetItem([l])
                qte.addChild(c)
            tvs += [qte]
        self._treeWidget.insertTopLevelItems(0, tvs)
        self._treeWidget.expandAll()


class TableSearcher(QtCore.QObject):  # TODO:横竖反了，想紫砂了
    def __init__(self, search_bar: QtWidgets.QLineEdit):
        super().__init__(parent=search_bar)
        self._orig_list = list()
        self._tableWidget = None
        self.parent().textChanged.connect(self.search)

    def setOrigList(self, lis: list):
        self._orig_list = lis

    def origList(self) -> list:
        return self._orig_list

    def setTableWidget(self, tab: QtWidgets.QListWidget):
        self._tableWidget = tab

    def tableWidget(self) -> QtWidgets.QTableWidget:
        return self._tableWidget

    @staticmethod
    def searchedList(orig: list, text: str):
        out = list()
        set_index = list()
        set_index.append(0)
        for i in range(len(orig)):
            for j in range(len(orig[i])):
                if text in orig[i][j]:
                    set_index.append(j)
        _j2l = list()
        for i2 in range(len(orig)):
            _j2l = list()
            for j2 in range(len(orig[i2])):
                if j2 in set_index:
                    _j2l.append(orig[i2][j2])
            if not _j2l:
                continue
            out.append(_j2l)
        return out

    def search(self):
        self.setData(self.searchedList(self._orig_list, self.parent().text()))

    def setData(self, data):
        assets_data: list = data
        self._tableWidget.clear()
        self._tableWidget.setColumnCount(len(assets_data))
        if assets_data[0]:
            self._tableWidget.setRowCount(len(assets_data[0]) - 1)
        vlabel = list()
        index = 0
        for i in assets_data:
            for j in range(len(i)):
                if not j:
                    vlabel.append(i[j])
                    continue
                item = QtWidgets.QTableWidgetItem(i[j])
                self._tableWidget.setItem(j - 1, index, item)
            index += 1
        self._tableWidget.setHorizontalHeaderLabels(vlabel)
        self._tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
