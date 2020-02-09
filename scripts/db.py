from peewee import *

db = SqliteDatabase('pypi.db')


class BaseModel(Model):
    class Meta:
        database = db


class Package(BaseModel):
    name = CharField(index=True, unique=True)
    metadata = TextField(null=True)


db.connect()
db.create_tables([Package])
