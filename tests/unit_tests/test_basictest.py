from unittest import TestCase

from flask import Flask

from core import create_app

class BasicTestTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        pass

    def test_basic_test(self):
        self.assertTrue(isinstance(self.app, Flask))

    def test_app_config(self):
        self.assertEqual(self.app.config['TESTING'], True)
        
