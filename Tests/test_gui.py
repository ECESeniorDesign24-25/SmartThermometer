import os
import unittest
from unittest import mock
from flask import Flask
from flask_testing import TestCase
from GUI import app
import sys


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_DIR = os.path.join(CURR_DIR, "..", "GUI")
sys.path.insert(0, os.path.abspath(GUI_DIR))

class FlaskAppTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    # Test the home route
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Temperature Graph - Two Sensors", response.data)

    # Test the temperature endpoint
    def test_temperature1_endpoint(self):
        response = self.client.get('/temperature')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['temperature1'], 20)
        self.assertEqual(data['temperature2'], 30)
        self.assertEqual(data['tempscale'], 'F')

    # Test the power on/off routes
    def test_power_on(self):
        with unittest.mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            response = self.client.get('/toggle2')
            self.assertEqual(response.status_code, 201)

    def test_power_off(self):
        with unittest.mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            response = self.client.get('/toggle1')
            self.assertEqual(response.status_code, 201)

    # Test the user info endpoint
    def test_user_info(self):
        response = self.client.get('/user?carrier=CarrierTest&phone=12345&email=test@example.com')
        self.assertEqual(response.status_code, 201)

    # Test min/max temperature endpoint
    def test_min_max_temp(self):
        response = self.client.get('/max_min?min=10&max=30')
        self.assertEqual(response.status_code, 201)

    # Test scale switching
    def test_switch_scale(self):
        response = self.client.get('/switch_scale')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn(data['unit'], ['C', 'F'])


if __name__ == "__main__":
    unittest.main()
