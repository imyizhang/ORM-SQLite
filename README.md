# ORM-SQLite

ORM-SQLite is

* a lightweight ORM for SQLite
* written in [Python (3.7+) Standard Library](https://docs.python.org/3.7/library/)



## Quickstart

1. Define a `Pomodoro` model

   ```python
   import orm_sqlite  

   class Pomodoro(orm_sqlite.Model):  

       id = orm_sqlite.IntegerField(primary_key=True) # auto-increment
       task = orm_sqlite.StringField()
       interval = orm_sqlite.IntegerField()
   ```

2. Create a `Database` instance

   ```python
   db = orm_sqlite.Database('example.db')
   ```

3. Set it as backend of `Pomodoro` model objects, CRUD operations thus can be performed later

   ```python
   Pomodoro.objects.backend = db
   ```

4. **Create** a Pomodoro timer record (primary key is auto-increment) and **insert** it to backend (**auto-commited**)

   ```python
   pomodoro = Pomodoro({'task': 'do something', 'interval': 25})
   pomodoro.save()
   ```

   which is equivalent to

   ```python
   pomodoro = Pomodoro({'task': 'do something', 'interval': 25})
   Pomodoro.objects.add(pomodoro)   
   ```

5. **Retrieve** all the records in the backend

   ```Python
   Pomodoro.objects.all()
   ```

6. **Retrieve** single record by its primary key and **update** it (**auto-commited**)

   ```python
   obj = Pomodoro.objects.get(pk=1)
   obj['task'] = 'do something else'
   obj.update()
   ```

   which is equivalent to

   ```python
   obj = Pomodoro.objects.get(pk=1)
   obj['task'] = 'do something else'
   Pomodoro.objects.update(obj)
   ```

7. **Retrieve** single record by its primary key and **delete** it (**auto-commited**)

   ```python
   Pomodoro.objects.get(pk=1).delete()
   ```

   which is equivalent to

   ```python
   obj = Pomodoro.objects.get(pk=1)
   Pomodoro.objects.remove(obj)
   ```

8. Disconnect the backend

   ```python
   Pomodoro.objects.backend.close()
   ```



### Install ORM-SQLite

```bash
$ pip install orm-sqlite
```



## Documentation

### Module `Database`

```python
class orm_sqlite.Database(database[, timeout, detect_types, isolation_level, check_same_thread, factory, cached_statements, uri])
```

* `connected`

  **Instance attribute**: Whether or not the SQLite database is connected.

* `connection`

  **Instance attribute**: `sqlite3.Connection` object

* `cursor`

  **Instance attribute**: `sqlite3.Cursor` object

* `connect()`

  **Instance method**: Connects the SQLite database if disconnected.

* `close()`

  **Instance method**: Disconnects the SQLite database if connected.

* `select(sql, *args, size=None)`

  **Instance method**: Returns query results, a list of `sqlite3.Row` objects.

* `execute(sql, *args, autocommit=True)`

  **Instance method**: Executes an SQL statement and returns rows affected.

* `commit()`

  **Instance method**: Commits the staged transaction.



### Module `StringField`

```python
class orm_sqlite.StringField(name=None, default='')
```

* `name`

  **Instance attribute**: Column name. Default: `None`.

* `type`

  **Instance attribute**: Column type. Default: `TEXT`.

* `default`

  **Instance attribute**: Column default value. Default: `''`.

* `primary_key`

  **Instance attribute**: Whether or not it is the primary key. Default: `False`.



### Module `IntegerField`

```python
class orm_sqlite.IntegerField(name=None, default=0, primary_key=False)
```

* `name`

  **Instance attribute**: Column name. Default: `None`.

* `type`

  **Instance attribute**: Column type. Default: `INTEGER`.

* `default`

  **Instance attribute**: Column default value. Default: `0`.

* `primary_key`

  **Instance attribute**: Whether or not it is the primary key. Default: `False`.



### Module `FloatField`

```python
class orm_sqlite.StringField(name=None, default=0.0)
```

* `name`

  **Instance attribute**: Column name. Default: `None`.

* `type`

  **Instance attribute**: Column type. Default: `REAL`.

* `default`

  **Instance attribute**: Column default value. Default: `0.0`.

* `primary_key`

  **Instance attribute**: Whether or not it is the primary key. Default: `False`.



### Module `Model`

```python
class orm_sqlite.Model(*args, **kwargs)
```

* `__table__`

  **Class attribute**: Table.

* `__mappings__`

  **Class attribute**: Object Relational Mappings (ORMs).

* `__primary_key__`

  **Class attribute**: Primary key.

* `__fields__`

  **Class attribute**: Fields except primary key.

* `objects`

  **Class-only attribute**: `orm_sqlite.Manager` object used to manage corresponding `Model` objects.

* `exists()`

  **Class-only method**: Whether or not the table exists in the connected database.

* `create()`

  **Class-only method**: Create the table if not exists in the connected database.

* `drop()`

  **Class-only method**: Drop the table if exists in the connected database, `objects.backend.commit()` needed to confirm. ***Extremely Dangerous***.

* `save()`

  **Instance method**: Inserts `Model` object to table in the connected database and returns rows affected (1 or -1).

* `update()`

  **Instance method**: Updates `Model` object from table in the connected database and returns rows affected (1 or -1). ***Dangerous***.

* `delete()`

  **Instance method**: Deletes `Model` object from table in the connected database and returns rows affected (1 or -1). ***Dangerous***.

* `keys()`, `values()`, `items()`,  `copy()`, etc. methods inherited from standard `dict`.



**Practical template for customized model**:

```python
import orm_sqlite

class MyModel(orm_sqlite.Model):

    id = orm_sqlite.IntegerField(primary_key=True) # auto-increment
    # TODO:   
```



### Module `Manager`

```python
class orm_sqlite.Manager()
```

* `backend`

  **Instance attribute**: `orm_sqlite.Database` object serving as backend of  `Model` objects.

* `all()`

  **Instance method**: Returns all `Model` objects from table in the connected database.

* `find(filter=None, order_by=None, **extra)`

  **Instance method**: Returns all `Model` objects satified the conditions from table in the connected database.

* `get(pk)`

  **Instance method**: Returns single `Model` object by its primary key from table in the connected database.

* `exists(pk)`

  **Instance method**: Whether or not a primary key exists in the table from the connected database.

* `aggregate(self, expression, filter=None)`

  **Instance method**: Returns the result of an aggregate function performed on table in the connected database.

* `add(obj)`

  **Instance method**: Inserts `Model` object to table in the connected database and returns rows affected (1 or -1).

* `update(obj)`

  **Instance method**: Updates `Model` object from table in the connected database and returns rows affected (1 or -1). ***Dangerous***.

* `remove(obj)`

  **Instance method**: Deletes `Model` object from table in the connected database and returns rows affected (1 or -1). ***Dangerous***.

* `clear()`

  **Instance method**: Deletes **all** `Model` objects from table in the connected database and returns rows affected (1 or -1), `backend.commit()` needed  to confirm. ***Extremely Dangerous***.



### Helper Function

* `root_logger(log_dir='.')`

  Returns root logger, a `logging.logger` object, logging in main module.

* `child_logger(child)`

  Returns child logger, a `logging.logger` object, logging in auxiliary module.



## Related Projects

* Inspired by [Django](https://www.djangoproject.com/) ORM
