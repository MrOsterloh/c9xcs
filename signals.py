from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    getDBItem = pyqtSignal(int)
    getDBLength = pyqtSignal()
    getDBKeys = pyqtSignal()


    def __init__(self, parent, *args, **kwargs):
        super(Signals, self).__init__(parent, *args, **kwargs)

        self.cache = None


    def emit(self, signal, data=None):
        self.cache = None
        signal.emit(data)
        return self.cache
