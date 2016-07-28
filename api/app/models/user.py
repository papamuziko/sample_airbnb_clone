import hashlib
import peewee

from app.models.base import BaseModel

'''
 User:
    - email: unique
    - password: should be set with MD5 ValueError
    - first_name: mandatory
    - last_name: mandatory
    - is_admin: mandatory and by default False
'''
class User(BaseModel):
    
    email = peewee.CharField(128, null = False, unique = True, index=True)
    password = peewee.CharField(128, null = False, default = "")
    first_name = peewee.CharField(128, null = False)
    last_name = peewee.CharField(128, null = False)
    is_admin = peewee.BooleanField(default = False)

    def set_password(self, clear_password):
        self.password = hashlib.md5(clear_password).hexdigest()

    def to_dict(self):
        return { 
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'email': self.email
                }