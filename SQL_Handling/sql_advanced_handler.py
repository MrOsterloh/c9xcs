"""

Bastian
created  23.05.2018

"""


import sqlite3
from SQL_Handling.sql_handler import SQLHandler


class SQLAdvanced_handler(SQLHandler):
    def __init__(self):
        super(SQLAdvanced_handler, self).__init__()
        self.create_main_table(["path"])
        self.create_keyword_table()

    def create_keyword_table(self):
        with self.conn:
            self.c.execute("CREATE TABLE keywords (key_id INTEGER PRIMARY KEY, key TEXT)")
            self.c.execute("CREATE TABLE cons (key_id INTEGER PRIMARY KEY, id INTEGER)")

    def insert_values_with_keys(self, value, keywords):
        with self.conn:
            self.c.execute("INSERT INTO " + self.main_table_name + " VALUES (null, 'hallo/ich/') ")
            self.c.execute("SELECT last_insert_rowid()")
            id = self.c.fetchone()
            for keyword in keywords:
                self.c.execute("INSERT INTO keywords VALUES (null, ?)", [keyword])
                self.c.execute("INSERT INTO cons VALUES (null, ?)", id)

if __name__ == "__main__":
    sqlhandler = SQLAdvanced_handler()
    value = 'HASD/ASDSAD/DASD/ASDASD/hallo'
    keys = ['hallo', 'ich','bin', 'es']
    sqlhandler.insert_values_with_keys(value, keys)
    sqlhandler.insert_values_with_keys(value, keys)
    sqlhandler.insert_values_with_keys(value, keys)
    sqlhandler.insert_values_with_keys(value, keys)
    sqlhandler.c.execute("SELECT * FROM  " + sqlhandler.main_table_name)
    print(sqlhandler.c.fetchall())
    sqlhandler.c.execute("SELECT * FROM  cons")
    print(sqlhandler.c.fetchall())
    sqlhandler.c.execute("SELECT * FROM keywords")
    print(sqlhandler.c.fetchall())
