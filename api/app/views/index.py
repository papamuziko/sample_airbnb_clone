from datetime import datetime

from app import *
from app.models.base import database


@app.route('/', methods=['GET'])
@as_json
def index():
    return { 'status': "OK", 'utc_time': datetime.utcnow(), 'time': datetime.now() }


# Database management
@app.before_request
def before_request(): 
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response


# Invalid path
@app.errorhandler(404)
@as_json
def not_found(e):
    return { 
        'code': 404, 
        'msg': "Not found" 
        }, 404 