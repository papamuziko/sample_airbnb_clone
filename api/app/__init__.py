from flask import Flask
from flask_json import FlaskJSON, as_json, request
from peewee import IntegrityError

app = Flask(__name__)
json = FlaskJSON(app)

from app.views import * 
