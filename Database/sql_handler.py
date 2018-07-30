import sqlite3
from PyQt5.QtCore import QObject, pyqtSlot


class SQLHandler(QObject):
    db_name = 'Messungen.db'

    def __init__(self, parent):
        super(SQLHandler, self).__init__(parent)

        self.conn = sqlite3.connect(':memory:')
        self.cur = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON")

        self.__colNames = list()
        self.__qHolder = str()

        with self.conn:
            self.cur.execute("CREATE TABLE IF NOT EXISTS main (ID INTEGER NOT NULL PRIMARY KEY, name TEXT)")
            self.cur.execute("CREATE TABLE IF NOT EXISTS keys (ID INTEGER NOT NULL PRIMARY KEY, key_name TEXT, tab_name TEXT)")

    def addItem(self, **kwargs):
        with self.conn:
            self.cur.execute("INSERT INTO main (name) VALUES (NULL)")
            self.cur.execute("SELECT last_insert_rowid() FROM main")
            id = str(self.cur.fetchone()[0])


            for key in kwargs:
                # search for tab with the key
                self.cur.execute("SELECT ID FROM keys WHERE key_name = '" + key + "'")
                if not self.cur.fetchone():
                    self.cur.execute("SELECT MAX(ID) from keys")
                    key_id = self.cur.fetchone()[0]
                    if not key_id:
                        key_id = '1'
                    else:
                        key_id = str(key_id + 1)
                    tab_name = 'tab' + key_id
                    print(key)
                    self.cur.execute("INSERT INTO keys (key_name, tab_name) VALUES ('" + key + "', '" + tab_name + "')")
                    self.cur.execute("SELECT last_insert_rowid() FROM keys")
                else:
                    self.cur.execute("SELECT ID FROM keys WHERE key_name = '" + key + "'")
                    key_id = str(self.cur.fetchone()[0])
                    tab_name = 'tab' + key_id

                self.cur.execute("CREATE TABLE IF NOT EXISTS " + tab_name + " (ID INTEGER NOT NULL PRIMARY KEY, key_ID INTEGER NOR NULL, value STRING NOT NULL, FOREIGN KEY(ID) REFERENCES main(ID) ON DELETE CASCADE, FOREIGN KEY(key_ID) REFERENCES keys(ID) ON DELETE CASCADE)")
                self.cur.execute("INSERT INTO " + tab_name + " (ID, key_ID, value) VALUES (" + id + ", " + key_id + ", '" + str(kwargs[key]) +"')")

        self.cur.execute("SELECT * FROM main")
        print(self.cur.fetchall())


        self.cur.execute("SELECT * FROM keys")
        print(self.cur.fetchall())

        self.cur.execute("SELECT * FROM tab1")
        print(self.cur.fetchall())

if __name__ == '__main__':
    main = SQLHandler(None)
    a = {'alias':"hunger", 'dedu':"DOPE"}
    main.addItem(**a)
    main.addItem(**a)
    main.addItem(**a)
    main.addItem(**a)

