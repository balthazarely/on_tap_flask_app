from peewee import *
from flask_login import UserMixin
import datetime
import os
from playhouse.db_url import connect

# DATABASE = PostgresqlDatabase('beer_app')
DATABASE = connect(os.environ.get('DATABASE_URL'))
class BaseModel(Model):
    class Meta: database = DATABASE


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField(unique=True)
    comments = CharField(null=True)
    modal = CharField(null=True)


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

