from PyQt5 import QtWidgets, QtCore
from MessUbersicht.Sheets.plot import MyView
from MessUbersicht.Sheets.table import MyTableSideWidget
from MessUbersicht.signals import Signals

from MessUbersicht.EGPE_FileFinder.fileWalker import DB

from MessUbersicht.Database.sql_handler import SQLHandler

class Main_window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main_window, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self._sig = Signals(self)
        self._sql = SQLHandler(self)
        #  Test File import
        self.tempSQL_filler()

        self.view = MyView(self, self._sig)
        self.table = MyTableSideWidget(self, self._sig)

        centralWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.addWidget(self.view)
        centralWidget.addWidget(self.table)
        centralWidget.setCurrentWidget(self.table)

        menuBar = self.menuBar()
        db_menu = menuBar.addMenu("Datenbasis")
        self.ac_dbRelaod = QtWidgets.QAction("Neu Laden")
        self.ac_dbOpen = QtWidgets.QAction("Öffnen")

        db_menu.addAction(self.ac_dbRelaod)
        db_menu.addAction(self.ac_dbOpen)

        pg_menu = menuBar.addMenu("Pages")
        self.pg_1 = QtWidgets.QAction("1")
        self.pg_1.triggered.connect(lambda: self.setPage(1))
        self.pg_2 = QtWidgets.QAction("2")
        self.pg_2.triggered.connect(lambda: self.setPage(2))

        pg_menu.addAction(self.pg_1)
        pg_menu.addAction(self.pg_2)

    def setPage1(self):
        self._sig.setPage.emit(1)
    def setPage2(self):
        self._sig.setPage.emit(2)

    @QtCore.pyqtSlot(int)
    def setPage(self, nr):
        w = self.centralWidget().widget(nr)
        if w:
            self.centralWidget().setCurrentWidget(w)

    def tempSQL_filler(self):
        db =DB(r'C:\Users\Bastian\Desktop\pytemp\MessUbersichtUbersicht.dmp')
        whitelist =[]
        for entry in db._data:
            whitedict = {}
            for key in entry:
                if isinstance(key, str):
                    new_key = key.replace('/','_').replace(' ','_').replace('-','_').replace('(','_').replace(')','_')
                    whitedict[new_key] = entry[key]
            whitelist.append(whitedict)
        for entry in whitelist:
            self._sql.addItem(**entry)

if __name__ == '__main__':
    import sys
    from PyQt5 import  QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec_())