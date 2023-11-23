import orm_sqlite


class Messages(orm_sqlite.Model):
	id = orm_sqlite.IntegerField(primary_key=True)
	game = orm_sqlite.IntegerField()
	inicial = orm_sqlite.IntegerField()
	mensagem = orm_sqlite.StringField()
