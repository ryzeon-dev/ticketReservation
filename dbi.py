import sqlite3

class DB:
    def __init__(self):
        self.db = sqlite3.connect('./db/db.db')
        self.cursor = self.db.cursor()

    def exec(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.db.close()

    def commit(self):
        self.db.commit()

def dbExecAndFetch(query):
    db = DB()

    db.cursor.execute(query)
    res = db.cursor.fetchall()

    db.close()
    return res