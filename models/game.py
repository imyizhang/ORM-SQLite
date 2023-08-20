import orm_sqlite


class Game(orm_sqlite.Model):
	id = orm_sqlite.IntegerField(primary_key=True)
	name = orm_sqlite.StringField()
	channel_aguardando_wl = orm_sqlite.StringField()
	channel_aprovados = orm_sqlite.StringField()
	channel_reprovados = orm_sqlite.StringField()
	role_aguardando_wl = orm_sqlite.StringField()
	role_aprov = orm_sqlite.StringField()
	role_cidadao = orm_sqlite.StringField()
	
	__table__ = "games"
