"""
Bastian

29.05.2018

"""

from sql_handler import SQLHandler
from file_handler import File_handler
from xml_handler import Xml_handler
import os

class Main(object):

    def __init__(self):
        self._file_types, self._file_types_index, self._keywords = list(), list(), list()
        self._path = os.getcwd()


        self.sql_handler = SQLHandler(self)
        self.file_handler = File_handler(self)
        self.xml_handler = Xml_handler(self)

        self.file_handler.start_walk()



    @property
    def path(self):
        return self._path
    @property
    def file_types(self):
        return self._file_types

    @file_types.setter
    def file_types(self, value):
        self._file_types = value

    @property
    def file_types_index(self):
        return self._file_types_index

    @file_types_index.setter
    def file_types_index(self, value):
        self._file_types_index = value

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        self._keywords = value

        #ToDo: xml: alle Fahrzeug attribute
        # file arten
            # endung
                # key words
                    # atttribute positionen

        self.collect_database()

    def collect_database(self):
        pass

if __name__ == '__main__':
    main = Main()
