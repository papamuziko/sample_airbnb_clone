##Sample AirBnB Clone

First steps of the AirBnB clone project written in Python with Flask.


###Run

```
$ python api/app.py
```

Don't forget to set correctly MySQL configuration (`api/config.py`)


###Tests:

```
$ cd api
api/ $ AIRBNB_ENV=test python -m unittest discover tests --pattern=*.py
```