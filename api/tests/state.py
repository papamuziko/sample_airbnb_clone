import os
import unittest
from flask import json
import peewee
import logging

from app import app
from app.models.base import database
from app.models.state import State


class StateTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.create_tables([State], safe=True)
        
    def tearDown(self):
        State.drop_table()

    def test_create(self):
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)

        # test another state
        res = self.app.post('/states', data={ 'name': "Arizona" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 2)

        # test duplicate
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 409)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['code'], 10001)
        

    def test_list(self):
        res = self.app.get('/states') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)
        
        # create one state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)

        # check if I have one state
        res = self.app.get('/states') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

    
    def test_get(self):
        res = self.app.get('/states/1')
        self.assertEqual(res.status_code, 404)
        
        # create a state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # get new state
        res = self.app.get('/states/%d' % current_state_id)
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], current_state_id)


    def test_delete(self):
        res = self.app.delete('/states/1')
        self.assertEqual(res.status_code, 404)
        
        # create a state
        res = self.app.post('/states', data={ 'name': "California" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_state_id = json_data['id']

        # number of states
        res = self.app.get('/states') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

        # delete new state
        res = self.app.delete('/states/%d' % current_state_id)
        self.assertEqual(res.status_code, 200)
        
        # number of states
        res = self.app.get('/states') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)

