from MessUbersicht.template_loader import loader_TemplateBasis_180305

import os, re, datetime
import pickle
from PyQt5.QtCore import pyqtSlot, QObject

def file_walker(start_path):
    for entry in os.scandir(start_path):
        if not entry.name.startswith('.') and entry.is_dir(follow_symlinks=False):
            yield from file_walker(entry.path)
        else:
            yield entry.path

class DB(QObject):
    def __init__(self, parent, sig, filename):
        super(DB, self).__init__()
        self._data = list()
        self._sig = sig

        sig.getDBItem.connect(self.getDBItem)
        sig.getDBLength.connect(self.getDBLength)
        sig.getDBKeys.connect(self.getBDKeys)


        if os.path.isfile(filename):
            self._data = self.load_from_pickle(filename)
            print("loaded db successfully")
        elif os.path.isdir(filename):
            print("starting to search for data")
            print("dir: %s" % filename)

        else:
            print("DB Error: filename does not exist")

    def search(self, start_path=None):
        if not start_path:
            start_path = r'\\vw.vwg\vwdfs\K-E\EG\1534\Groups\EGPE-4\03_Messung\02_BEV' + os.sep

        for nr, path in enumerate(file_walker(start_path)):
            if re.search(r'.*Auswertung_.*\.xlsb', path):
                try:
                    result = loader_TemplateBasis_180305(path)
                    if isinstance(result, dict):
                        self._data.append(result)
                        if len(self.file_list)> 100:
                            break
                except Exception as err:
                    print("DB Error: continue")

        if not start_path:
            path = start_path + os.sep + 'MeasDB_' + datetime.datetime.now()
        else:
            path = os.getcwd() + os.sep + 'MeasDB_' + datetime.datetime.now()

        with open(path, 'wb') as file:
            pickle.dump(self._data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def load_from_pickle(self, filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)

    @pyqtSlot(int, result= dict)
    def getDBItem(self, nr):
        try:
            self._sig.cache = self._data[nr]
        except KeyError:
            print("DB does not have item of nr %s" %nr)

    @pyqtSlot(result=int)
    def getDBLength(self):
        self._sig.cache = len(self._data)

    @pyqtSlot(result=list)
    def getBDKeys(self):
        keys = list()
        for item in self._data:
            for key in item:
                if key not in keys and isinstance(key, str):
                    keys.append(key)
        self._sig.cache = keys




if __name__ == '__main__':
    start_path = r'\\vw.vwg\vwdfs\K-E\EG\1534\Groups\EGPE-4\03_Messung\02_BEV'

    db = DB()
    # db.reload()
    db.load_from_pickle()

    print(db.file_list)