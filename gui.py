from PyQt5 import QtWidgets, QtGui, QtCore
from MessUbersicht.plot import MyView
from MessUbersicht.table import MyTableSideWidget
from MessUbersicht.signals import Signals
from MessUbersicht.database import DB


class Main_window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main_window, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._sig = Signals(self)
        self._db = DB(self, self._sig, r'C:\Users\ea5pqvh\Desktop\pytemp\MessUbersichtUbersicht.dmp')
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
        self.pg_1.triggered.connect(self.setPage1)
        self.pg_2 = QtWidgets.QAction("2")
        self.pg_2.triggered.connect(self.setPage2)

        pg_menu.addAction(self.pg_1)
        pg_menu.addAction(self.pg_2)


    def setPage1(self, nr=None):
        if not nr:
            nr = 1
        self.centralWidget().setCurrentWidget(self.table)

    def setPage2(self, nr=None):
        if not nr:
            nr = 2
        self.centralWidget().setCurrentWidget(self.view)


if __name__ == '__main__':
    import sys
    from PyQt5 import  QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec_())