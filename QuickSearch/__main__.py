"""

created 30.05.2018
"""


import sys

from os import scandir, getcwd
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QTableWidget, QCompleter
from PyQt5.Qt import QStringListModel

import os
from sql_handler import SQLHandler



class QuickSearch(object):
    def __init__(self):

        self.sql_handler = SQLHandler(None)
        self.sql_handler.create_table(["name", "path"])

        self.fill_table()
        self.get_values()

    def file_generator(self, path):
        for entry in scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.file_generator(entry.path)
            else:
                yield entry.path

    def fill_table(self):
        pathlist = ['\Training\PythonProjects\c9xcs\_Auswertung2_.xlsb', '\Training\PythonProjects\c9xcs\_Auswertung_.xlsx']
        for entry in pathlist:
            keywords = [entry.split(os.sep)[-1]]
            self.sql_handler.insert_values(name=keywords[0], path=entry)

    def get_values(self):
        print(self.sql_handler.get_fzg_by_name('_Auswertung2_.xlsb'))


if __name__ == '__main__':
    qSearch = QuickSearch()

