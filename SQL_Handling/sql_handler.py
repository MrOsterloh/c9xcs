"""

Bastian
created  23.05.2018

"""

import os
import sqlite3



class SQLHandler():

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        print("created conn")
        self.c = self.conn.cursor()
        self.main_table_name = "mtable"

        self.__colNames = list()
        self.__qHolder = str()

    def create_main_table(self, attributes):
        with self.conn:
            self.c.execute("CREATE TABLE " + self.main_table_name + " (id INTEGER PRIMARY KEY)")
            _type = 'TEXT'
            _default = ''
            for attribute in attributes:
                self.c.execute("ALTER TABLE  " + self.main_table_name + "  ADD %s %s %s" %(attribute, _type, _default))

            self.__colNames = tuple(attributes)
            self.__qHolder = '(' + '?' + ', ?'*(len(self.__colNames)-1) + ')'

    def insert_values(self, **kwargs):
        values = list()
        for colName in self.__colNames:
            if colName in kwargs:
                values.append(kwargs[colName])
                kwargs.pop(colName)
            else:
                values.append(str())
                print('Warning: Inserted values do not contain a valid entry for %s' %colName)
        if kwargs:
            for colName in kwargs:
                print('Warning: %s is not a valid entry in the table' %colName)
        if values:
            with self.conn:
                self.c.execute("PRAGMA table_info( " + self.main_table_name + " )")
                self.c.execute("INSERT INTO  " + self.main_table_name + " %s VALUES %s " % (self.__colNames, self.__qHolder), tuple(values))

    def get_entry_by_name(self, name):
        self.c.execute("SELECT * FROM  " + self.main_table_name + "  WHERE name=?",(name,))
        return self.c.fetchall()

    def update_name(self, old_name, new_name):
        while self.conn:
            self.c.execute("UPDATE  " + self.main_table_name + "  SET name = ? WHERE name LIKE ?", (new_name, '%'+old_name+'%'))


if __name__ == '__main__':
    from random import  randint
    main = SQLHandler()

    size = 100

    fzg_list = ['Golf' for i in range(size)]
    herst_list = ['vw' for i in range(size)]
    edit_list = [randint(0,999999) for i in range(size)]

    for name, her, edit in zip(fzg_list,herst_list,edit_list):
        main.insert_values(name=name, hersteller = her, edit=edit)

    print(main.get_fzg_by_name('Golf'))