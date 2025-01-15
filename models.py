# models.py
from peewee import *

db = SqliteDatabase('carsweb.db')

class Car(Model):
    name = CharField()
    brand = CharField()
    model = CharField()
    price = DecimalField()

    class Meta:
        database = db  # This model uses the "database.db" database.

# Buat tabel
db.connect()
db.create_tables([Car], safe=True)
