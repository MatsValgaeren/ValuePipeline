# DataBaseManager

from peewee import *

db = SqliteDatabase('database/ValuePipeline-Database.db')

# sqlite_db = SqliteDatabase('/path/to/app.db', pragmas={
#     'journal_mode': 'wal',
#     'cache_size': -1024 * 64})

class User(Model):
    id = IntegerField(unique=True)
    filename = CharField(null=True)
    filepath = CharField()
    creator = CharField()
    status = CharField()
    duration = IntegerField()

    class Meta:
        database = db
        table_name = 'files'

def add_item(filename, filepath, creator):
    q = User.insert(filename=filename, filepath=filepath, creator=creator)
    q.execute()

# rows=User.select()
# print (rows.sql())
# for row in rows:
#    print ("name: {} age: {}".format(row.id, row.creator))
# db.close()
