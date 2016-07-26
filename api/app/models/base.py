import peewee
import datetime

from config import *

# connector to MySQL
database = peewee.MySQLDatabase(host=DATABASE['host'], 
    user=DATABASE['user'],
    password=DATABASE['password'],
    database=DATABASE['database'],
    port=DATABASE['port'],
    charset=DATABASE['charset'])

'''
 BaseModel:
    - id: primary key
    - created_at: datetime when a new resource is created
    - updated_at: datetime when a resource is updated (via overloading save method)
'''
class BaseModel(peewee.Model):

    id = peewee.PrimaryKeyField(unique=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now, formats="%Y/%m/%d %H:%M:%S")
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, formats="%Y/%m/%d %H:%M:%S")
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = database
        order_by = ('id', )

