from peewee import *

db = SqliteDatabase('database/vp-db.sql')

class BaseModel(Model):
    class Meta:
        database = db

cursor = db.execute_sql('SELECT * FROM your_table_name')
rows = cursor.fetchall()
for row in rows:
    print(row)