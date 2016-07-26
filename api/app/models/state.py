import hashlib
import peewee

from app.models.base import BaseModel

'''
 State:
    - name: unique
'''
class State(BaseModel):
    
    name = peewee.CharField(128, null = False, index = True, unique = True)
    
    def to_hash(self):
        return { 
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'name': self.name
                }