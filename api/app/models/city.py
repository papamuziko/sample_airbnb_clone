import hashlib
import peewee

from app.models.base import BaseModel
from app.models.state import State

'''
 City:
    - name: not unique but unique in a state 
    - state: foreign key to a state
'''
class City(BaseModel):
    
    name = peewee.CharField(128, null = False, index=True)
    state = peewee.ForeignKeyField(State, related_name="cities", on_delete="CASCADE")

    def to_hash(self):
        return { 
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'name': self.name,
                'state_id': self.state.id
                }