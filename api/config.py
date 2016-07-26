import os

AIRBNB_ENV = os.environ.get('AIRBNB_ENV')

# common values for Database configuration
DATABASE = {
    'host': "localhost",
    'port': 3306,
    'charset': "utf8",
}

# by default, always in development
DEBUG = True
HOST = "localhost"
PORT = 3333
DATABASE['user'] = "airbnb_user_dev"
DATABASE['database'] = "airbnb_dev"
DATABASE['password'] = os.environ.get('AIRBNB_DATABASE_PWD_DEV')

# Production configuration
if AIRBNB_ENV == "production":
    DEBUG = False
    HOST = "localhost"
    PORT = 3000
    DATABASE['user'] = "airbnb_user_prod"
    DATABASE['database'] = "airbnb_prod"
    DATABASE['password'] = os.environ.get('AIRBNB_DATABASE_PWD_PROD')

# Test configuration
elif AIRBNB_ENV == "test":
    DEBUG = False
    HOST = "localhost"
    PORT = 5556
    DATABASE['user'] = "airbnb_user_test"
    DATABASE['database'] = "airbnb_test"
    DATABASE['password'] = os.environ.get('AIRBNB_DATABASE_PWD_TEST')
