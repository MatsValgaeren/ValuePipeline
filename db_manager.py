# DataBaseManager

from peewee import *


db = SqliteDatabase('database/ValuePipeline-Database.db')

# sqlite_db = SqliteDatabase('/path/to/app.db', pragmas={
#     'journal_mode': 'wal',
#     'cache_size': -1024 * 64})

class User(Model):
    id = IntegerField(unique=True)
    filepath = CharField()
    filename = CharField(null=True)
    version = IntegerField()
    extension = CharField()


    create_datetime = DateTimeField(column_name='Create DateTime')
    upload_datetime = DateTimeField(column_name='Upload DateTime')

    creator = CharField()
    status = CharField()
    duration = IntegerField()

    width = IntegerField()
    height = CharField()

    iso = IntegerField()
    exposure = IntegerField()
    shutter = IntegerField()
    focal_length = IntegerField(column_name='Focal Length')

    project = CharField()
    sequence = IntegerField()
    shot = IntegerField()


    class Meta:
        database = db
        table_name = 'files'

def add_item(**kwargs):
    required = ['filename', 'filepath']

    for field in required:
        if field not in kwargs:
            raise ValueError(f"Missing required field: {field}")
    print(kwargs)
    q = User.insert(**kwargs)
    q.execute()

def get_items():
    pass



# rows=User.select()
# print (rows.sql())
# for row in rows:
#    print ("name: {} age: {}".format(row.id, row.creator))
# db.close()
