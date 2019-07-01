from unittest import TestCase

from core import create_app

class UserTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        ## Drop database
        pass

    def test_user_registration(self):
        res = self.test_client.post(
            'http://localhost:5000/register',
            json = {
                'email': 'jonnieey@gmail.com',
                'username': 'jonnieey',
                'password': 'password'
            }
        )
        self.assertEqual(res.status_code, 201)
