import os
import unittest
from datetime import datetime
from flask import json

from app import app

class IndexTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        pass

    def test_200(self):
        res = self.app.get('/') 
        self.assertEqual(res.status_code, 200)

    def test_status(self):
        res = self.app.get('/')
        json_data = json.loads(res.data)
        self.assertEqual(json_data['status'], 'OK')

    def test_time(self):
        res = self.app.get('/')
        json_data = json.loads(res.data)
        time = json_data['time']
        d_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
        d_now = datetime.now()
        self.assertEqual(d_time.year, d_now.year)
        self.assertEqual(d_time.month, d_now.month)
        self.assertEqual(d_time.day, d_now.day)
        self.assertEqual(d_time.hour, d_now.hour)
        self.assertEqual(d_time.minute, d_now.minute)

    def test_time_utc(self):
        res = self.app.get('/')
        json_data = json.loads(res.data)
        time = json_data['utc_time']
        d_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
        d_now = datetime.utcnow()
        self.assertEqual(d_time.year, d_now.year)
        self.assertEqual(d_time.month, d_now.month)
        self.assertEqual(d_time.day, d_now.day)
        self.assertEqual(d_time.hour, d_now.hour)
        self.assertEqual(d_time.minute, d_now.minute)