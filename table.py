from PyQt5 import QtWidgets, QtGui, QtCore


class MyTableSideWidget(QtWidgets.QWidget):
    def __init__(self, parent, sig, *args, **kwargs):
        super(MyTableSideWidget, self).__init__(parent, *args, **kwargs)
        self._sig = sig

        layout = QtWidgets.QGridLayout()
        table = MyTableWidget(parent, sig)


        self.lists = QtWidgets.QListWidget(self)
        details = QtWidgets.QListWidget(self)

        layout.addWidget(self.lists, 0, 0)
        layout.addWidget(details, 1, 0)
        layout.addWidget(table, 0, 1, 2, 5)

        self.setLayout(layout)

        self.blacklist = ['hallo', ' ich'] # list()
        self.whitelist = list()

        # self.update_list()


    def upadet(self):
        if self.whitelist:
            for item in self.whitelist:
                item = QtWidgets.QListWidgetItem(item, self.lists)
        else:
            for item in self.blacklist:
                item = QtWidgets.QListWidgetItem(item, self.lists)

    def upadate_details(self):
        pass

    def update_table(self):
        pass

class FilterItem(object):
    def __init__(self, name, parentListWidget, parentDetailsWidget):

        self._name = name
        self._listItem = QtWidgets.QListWidgetItem(self._name, parentListWidget)
        self._IDs = []
        self._details = list()


class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, sig, *args, **kwargs):
        super(MyTableWidget, self).__init__(parent, *args, **kwargs)
        self._sig = sig


        self._sig.getDBKeys.emit()
        self.setRowCount(len(self._sig.cache))
        self.setVerticalHeaderLabels(self._sig.cache)

        self._v_header = self._sig.cache

        self._sig.getDBLength.emit()
        self.setColumnCount(self._sig.cache)

        print(self._sig.cache)
        for col in range(self._sig.cache):
            self.insertColumn(col)
            self._sig.getDBItem.emit(col)
            for row in range(self.rowCount()):
                for key in self._sig.cache:
                    if key == self._v_header[row]:
                        item = QtWidgets.QTableWidgetItem(self._sig.cache[key])
                        self.setItem(1,10, item)




