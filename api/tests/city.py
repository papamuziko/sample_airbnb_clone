import os
import unittest
from flask import json
import peewee
import logging

from app import app
from app.models.base import database
from app.models.state import State
from app.models.city import City


class CityTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.create_tables([State, City], safe=True)
        
    def tearDown(self):
        City.drop_table()
        State.drop_table()

    def test_create(self):

        # create the state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # create a city
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        
        # test another city
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Diego" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 2)

        # test duplicate wrong
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 409)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['code'], 10002)

        # create another state
        res = self.app.post('/states', data={ 'name': "Arizona" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 2)
        current_state_id_2 = json_data['id']

        # test duplicate right
        res = self.app.post('/states/%d/cities' % current_state_id_2, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 3)

        # test unknow state
        res = self.app.post('/states/10/cities', data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 404)
        

    def test_list(self):
        
        # create the state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # empty list
        res = self.app.get('/states/%d/cities' % current_state_id) 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)
        
        # create one city
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 201)

        # check if I have one city
        res = self.app.get('/states/%d/cities' % current_state_id) 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

    
    def test_get(self):
        
        # create the state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # test unknow city
        res = self.app.get('/states/%d/cities/1' % current_state_id)
        self.assertEqual(res.status_code, 404)
        
        # create a city
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_city_id = json_data['id']

        # get new state
        res = self.app.get('/states/%d/cities/%d' % (current_state_id, current_city_id))
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], current_city_id)


    def test_delete(self):
        
        # create the state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # test unknow city
        res = self.app.delete('/states/%d/cities/1' % current_state_id)
        self.assertEqual(res.status_code, 404)
        
        # create a city
        res = self.app.post('/states/%d/cities' % current_state_id, data={ 'name': "San Francisco" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_city_id = json_data['id']

        # number of states
        res = self.app.get('/states/%d/cities' % current_state_id) 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

        # delete new state
        res = self.app.delete('/states/%d/cities/%d' % (current_state_id, current_city_id))
        self.assertEqual(res.status_code, 200)
        
        # number of states
        res = self.app.get('/states/%d/cities' % current_state_id) 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)

