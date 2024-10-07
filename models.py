from peewee import *
import datetime

# Initialize the SQLite database
db = SqliteDatabase('users.db')

class BaseModel(Model):
    class Meta:
        database = db

class Group(BaseModel):
    name = CharField()
    group_id = CharField(unique=True)

# Define the User BaseModel with a self-referential relationship for referrals
class User(BaseModel):
    user_id = CharField(unique=True)
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField(null=True)
    datetime = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    is_registrar = BooleanField(default=False)

class Member(BaseModel):
    user = ForeignKeyField(User, backref='members', on_delete='CASCADE')
    referrer = ForeignKeyField('self', null=True, backref='referrals', on_delete='SET NULL', default=None)
    group = ForeignKeyField(Group, backref='members',on_delete='CASCADE')
    is_joined = BooleanField(default=True)


# Create the table
db.connect()

if __name__ == '__main__':
    db.create_tables([User, Group, Member])

    print("Tables created")

# User.create(user_id='5798300617',first_name='MD Muktadirul Islam',username='Muktadirul',last_name='Mahi',chat_id='5798300617', is_admin=True, is_registrar=True)
