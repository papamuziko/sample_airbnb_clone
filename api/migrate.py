import peewee

from app.models.base import database
from app.models.user import User
from app.models.city import City
from app.models.state import State

try:
    # important to user "create_tables" instead of "create_table", to create index and constraints
    database.create_tables([City, State, User], safe=True)
except peewee.OperationalError:
    pass

