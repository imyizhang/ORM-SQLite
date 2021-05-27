#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from .logger import child_logger

logger = child_logger('orm_sqlite.database')


class Database(object):

    _connection = None
    _cursor = None
    _connected = False

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connect()

    def connect(self):
        if not self._connected:
            self._connection = sqlite3.connect(*self.args, **self.kwargs)
            self._connection.row_factory = sqlite3.Row
            self._cursor = self._connection.cursor()
            self._connected = True
        logger.info('database connected')

    def close(self):
        if self._connected:
            self.connection.close()
            self._connected = False
        logger.info('database disconnected')

    @property
    def connected(self):
        return self._connected

    # `sqlite3.Connection` objects
    @property
    def connection(self):
        return self._connection

    # `sqlite3.Cursor` objects
    @property
    def cursor(self):
        return self._cursor

    def select(self, sql, *args, size=None):
        self.cursor.execute(sql, args)
        if size is None:
            result = self.cursor.fetchall()
        else:
            result = self.cursor.fetchmany(size=size)
        #rows_selected = self.cursor.rowcount
        rows_selected = len(result)
        logger.info('rows selected: {}'.format(rows_selected))
        return result

    def execute(self, sql, *args, autocommit=True):
        self.cursor.execute(sql, args)
        rows_affected = self.cursor.rowcount
        if autocommit:
            self.commit()
        logger.info('rows affected: {}'.format(rows_affected))
        return rows_affected

    def commit(self):
        self.connection.commit()
