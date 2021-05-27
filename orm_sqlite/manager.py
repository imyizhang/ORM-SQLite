#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .database import Database
from .logger import child_logger

logger = child_logger('orm_sqlite.manager')


class Manager(object):

    def __init__(self):
        self._database = None
        self._model = None

    @property
    def backend(self):
        return self._database

    @backend.setter
    def backend(self, database):
        if not isinstance(database, Database):
            raise ValueError('{} is not a Database object.'.format(database))
        self._database = database

    def as_attribute(self, cls, name='objects'):
        self._model = cls
        setattr(cls, name, ManagerDescriptor(self))

    # manage table

    def table_exists(self):
        sql = '''
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='{}';'''.format(
            self._model.__table__
        )
        logger.debug('\n    SQL: {}'.format(sql))
        result = self._database.select(sql)
        return True if len(result) == 1 else False

    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS {} (
            {} INTEGER PRIMARY KEY AUTOINCREMENT,
            {}
        );'''.format(
            self._model.__table__,
            self._model.__primary_key__,
            ',\n            '.join(self._model.__columns__)
        )
        logger.debug('\n    SQL: {}'.format(sql))
        return self._database.execute(sql)

    def drop_table(self):
        sql = '''
        DROP TABLE IF EXISTS {};'''.format(
            self._model.__table__
        )
        logger.debug('\n    SQL: {}'.format(sql))
        return self._database.execute(sql, autocommit=False)

    # retrieve data

    def all(self):
        sql = '''
        SELECT * FROM {};'''.format(
            self._model.__table__
        )
        logger.debug('\n    SQL: {}'.format(sql))
        results = self._database.select(sql)
        return [self._model(dict(r)) for r in results]

    def find(self, filter=None, order_by=None, **extra):
        sql = '''
        SELECT * FROM {}'''.format(
            self._model.__table__
        )
        if filter is not None:
            sql += '\n        WHERE {}'.format(filter)
        if order_by is not None:
            sql += '\n        ORDER BY {}'.format(order_by)
        # TODO:
        sql += ';'
        logger.debug('\n    SQL: {}'.format(sql))
        results = self._database.select(sql)
        return [self._model(dict(r)) for r in results]

    def get(self, pk):
        sql = '''
        SELECT * FROM {}
        WHERE {} = ?;'''.format(
            self._model.__table__,
            self._model.__primary_key__
        )
        args = [pk]
        logger.debug('\n    SQL: {}\n    ARGS:\n        {}'.format(sql, args))
        result = self._database.select(sql, *args)
        if len(result) == 1:
            return self._model(dict(result[0]))
        return None

    def exists(self, pk):
        obj = self.get(pk)
        return False if obj is None else True

    def aggregate(self, expression, filter=None):
        sql = '''
        SELECT {} FROM {}'''.format(
            expression,
            self._model.__table__
        )
        if filter is not None:
            sql += '\n        WHERE {}'.format(filter)
        sql += ';'
        logger.debug('\n    SQL: {}'.format(sql))
        result = self._database.select(sql)
        if len(result) == 1:
            return dict(result[0])
        return None

    # modify data

    def add(self, obj):
        if self._model.__primary_key__ in obj:
            if self.exists(obj[self._model.__primary_key__]):
                rows_affected = -1
                logger.info('rows affected: {}'.format(rows_affected))
                return rows_affected
            sql = '''
        INSERT INTO {} ({})
        VALUES ({});'''.format(
                self._model.__table__,
                ', '.join([self._model.__primary_key__] + self._model.__fields__),
                ', '.join(['?'] + self._model.__placeholders__)
            )
        else:
            sql = '''
        INSERT INTO {} ({})
        VALUES ({});'''.format(
                self._model.__table__,
                ', '.join(self._model.__fields__),
                ', '.join(self._model.__placeholders__)
            )
        args = list(obj.values())
        logger.debug('\n    SQL: {}\n    ARGS:\n        {}'.format(sql, args))
        return self._database.execute(sql, *args)

    def update(self, obj):
        sql = '''
        UPDATE {}
        SET {}
        WHERE {} = ?;'''.format(
            self._model.__table__,
            ', '.join([f + ' = ?' for f in self._model.__fields__]),
            self._model.__primary_key__
        )
        if (self._model.__primary_key__ not in obj) or (not self.exists(obj[self._model.__primary_key__])):
            rows_affected = -1
            logger.info('rows affected: {}'.format(rows_affected))
            return rows_affected
        copied_obj = obj.copy()
        pk = copied_obj.pop(self._model.__primary_key__)
        args = list(copied_obj.values()) + [pk]
        logger.debug('\n    SQL: {}\n    ARGS:\n        {}'.format(sql, args))
        return self._database.execute(sql, *args)

    def remove(self, obj):
        sql = '''
        DELETE FROM {}
        WHERE {} = ?;'''.format(
            self._model.__table__,
            self._model.__primary_key__
        )
        if (self._model.__primary_key__ not in obj) or (not self.exists(obj[self._model.__primary_key__])):
            rows_affected = -1
            logger.info('rows affected: {}'.format(rows_affected))
            return rows_affected
        args = [obj[self._model.__primary_key__]]
        logger.debug('\n    SQL: {}\n    ARGS:\n        {}'.format(sql, args))
        return self._database.execute(sql, *args)

    def clear(self):
        sql = '''
        DELETE FROM {};'''.format(
            self._model.__table__
        )
        logger.debug('\n    SQL: {}'.format(sql))
        return self._database.execute(sql, autocommit=False)


class ManagerDescriptor(object):

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via {} instances.".format(cls.__name__))
        return self.manager


class classonlymethod(classmethod):

    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via {} instances.".format(cls.__name__))
        return super().__get__(instance, cls)
