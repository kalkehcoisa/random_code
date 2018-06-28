#!/usr/bin/env python3

from tinydb import TinyDB, Query


class TinyDBManager:
    __db = None
    __instance = None

    Filter = Query()

    def __new__(cls, *ag, **kw):
        if cls.__instance is None:
            cls.__instance = super(TinyDBManager, cls).__new__(cls, *ag, **kw)
        return cls.__instance

    def __init__(self, db_name='ebooks.json', *ag, **kw):
        self.db_name = db_name
        type(self).__db = TinyDB(self.db_name)

    def check(self, column, value):
        '''
        Checks if the column with value doesn't exist in the database.
        '''
        return len(self.__db.search(
            getattr(self.Filter, column) == value)) == 0

    def insert(self, values):
        self.__db.insert(values)


if __name__ == '__main__':
    db = TinyDBManager()
    db.insert({'type': 'peach'})
    print(db.check('type', 'peach'))
