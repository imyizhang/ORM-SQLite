import orm_sqlite
from models.game import Game
from models.messages import Messages

db = orm_sqlite.Database('database.db')
Messages.objects.backend = db
x = Messages.objects.where(pk=1).find()
print(x.id)
