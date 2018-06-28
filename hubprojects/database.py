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

    def __init__(self, db_name='repositories.json', *ag, **kw):
        self.db_name = db_name
        type(self).__db = TinyDB(self.db_name)

    def search(self, column, value):
        return self.__db.search(getattr(self.Filter, column) == value)

    def exist(self, column, value):
        '''
        Checks if the column with value exist in the database.
        '''
        return self.__db.count(getattr(self.Filter, column) == value) > 0

    def insert(self, values):
        self.__db.insert(values)
