"""

Bastian
created  23.05.2018

"""


import sqlite3
from SQL_Handling.sql_handler import SQLHandler


class SQLKeyword_Handler(SQLHandler):
    def __init__(self):
        super(SQLKeyword_Handler, self).__init__()
        self.create_main_table(["path"])
        self.create_keyword_table()

    def create_keyword_table(self):
        with self.conn:
            self.c.execute("CREATE TABLE keywords (key_id INTEGER PRIMARY KEY, key TEXT)")
            self.c.execute("CREATE TABLE cons (key_id INTEGER, id INTEGER)")

    def Joins(self):
        self.c.execute("SELECT * FROM " + self.main_table_name + " INNER JOIN cons     ON cons.id = mtable.id")
        self.c.execute("SELECT * FROM cons                         INNER JOIN keywords ON keywords.key_id = cons.key_id")

    def insert_values_with_keys(self, value, keywords):
        with self.conn:
            self.c.execute("INSERT INTO " + self.main_table_name + " VALUES (null, ?)", [value])
            self.c.execute("SELECT last_insert_rowid()")
            id = self.c.fetchone()
            for keyword in keywords:
                self.c.execute("SELECT key_id FROM keywords WHERE key = ?", [keyword])
                key_id = self.c.fetchone()
                if key_id:
                    self.c.execute("INSERT INTO cons Values(?, ?)", key_id + id)
                else:
                    self.c.execute("INSERT INTO keywords VALUES (null, ?)", [keyword])
                    self.c.execute("SELECT last_insert_rowid()")
                    key_id = self.c.fetchone()
                    self.c.execute("INSERT INTO cons VALUES (?, ?)", key_id + id)


if __name__ == "__main__":
    sqlhandler = SQLKeyword_Handler()
    sqlhandler.insert_values_with_keys('path1', ['keyword1'])
    sqlhandler.insert_values_with_keys('path2', ['keyword1', 'keyword2'])
    sqlhandler.insert_values_with_keys('path3', ['keyword3'])

    sqlhandler.Joins()

    # step 1
    sqlhandler.c.execute("SELECT key FROM keywords")
    print(sqlhandler.c.fetchall())
    # setp 2
    sqlhandler.c.execute("SELECT key_id FROM keywords WHERE key = ? ", ["keyword1"])
    res = sqlhandler.c.fetchall()
    print(res)
    # step 3
    sqlhandler.c.execute("SELECT id FROM cons WHERE key_id = ? ", res[0])
    res = sqlhandler.c.fetchall()
    print(res)
    for result in res:
        sqlhandler.c.execute("SELECT path FROM mtable WHERE id = ? ", result)
        res = sqlhandler.c.fetchall()
        print('entering %s to table' %res)

    print('alternative')
    sqlhandler.c.execute("SELECT path FROM mtable "  
                         "INNER JOIN cons ON cons.id = mtable.id " +
                         "INNER JOIN keywords ON keywords.key_id = cons.key_id " +
                         "WHERE keywords.key = ?", ['keyword1'])
    res = sqlhandler.c.fetchall()
    print(res)
    # sqlhandler.c.execute("SELECT * FROM  " + sqlhandler.main_table_name)
    # print(sqlhandler.c.fetchall())
    # sqlhandler.c.execute("SELECT * FROM  cons")
    # print(sqlhandler.c.fetchall())
    # sqlhandler.c.execute("SELECT * FROM keywords")
    # print(sqlhandler.c.fetchall())
