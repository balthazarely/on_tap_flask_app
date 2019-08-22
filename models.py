from peewee import *
from flask_login import UserMixin
import datetime

# Connect to a Postgres database.
DATABASE = PostgresqlDatabase('beer_app')

class BaseModel(Model):
    """A base Model that will use our psql database"""
    class Meta: database = DATABASE


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField(unique=True)
    image = CharField()


class Beer(BaseModel):
    api_id = CharField()
    user_id = CharField()
    favorite = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)
    reviews = CharField()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Beer], safe=True)
    print("TABLES Created")
    DATABASE.close()

