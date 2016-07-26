import os
import unittest
from flask import json
import peewee
import logging

from app import app
from app.models.base import database
from app.models.user import User


class UserTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.create_tables([User], safe=True)
        
    def tearDown(self):
        User.drop_table()


    def test_create(self):
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)

        # test another user
        res = self.app.post('/users', data={ 'email': "aria@stark.com", 'first_name': "Aria", 'last_name': "Stark" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 2)

        # test duplicate
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 409)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['code'], 10000)
        

    def test_list(self):
        res = self.app.get('/users') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)
        
        # create one user
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 201)

        # check if I have one user
        res = self.app.get('/users') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

    
    def test_get(self):
        res = self.app.get('/users/1')
        self.assertEqual(res.status_code, 404)
        
        # create a user
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_user_id = json_data['id']

        # get new user
        res = self.app.get('/users/%d' % current_user_id)
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], current_user_id)


    def test_delete(self):
        res = self.app.delete('/users/1')
        self.assertEqual(res.status_code, 404)
        
        # create a user
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_user_id = json_data['id']

        # number of users
        res = self.app.get('/users') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 1)

        # delete new user
        res = self.app.delete('/users/%d' % current_user_id)
        self.assertEqual(res.status_code, 200)
        
        # number of users
        res = self.app.get('/users') 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['data']), 0)


    def test_update(self):
        res = self.app.put('/users/1', data={ 'first_name': "Jon Junior" })
        self.assertEqual(res.status_code, 404)
        
        # create a user
        res = self.app.post('/users', data={ 'email': "Jon@snow.com", 'first_name': "Jon", 'last_name': "Snow" })
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], 1)
        current_user_id = json_data['id']
        current_user_first_name = json_data['first_name']

        # update first_name
        res = self.app.put('/users/1', data={ 'first_name': "Jon Junior" }) 
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['id'], current_user_id)
        self.assertNotEqual(json_data['first_name'], current_user_first_name)

