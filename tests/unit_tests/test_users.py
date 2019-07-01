from unittest import TestCase

from core import create_app, db

USER = {
    'email': 'jonnieey@gmail.com',
    'username': 'jonnieey',
    'password': 'password'
}

class UserTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        ## Drop database
        current_db = self.app.config['MONGODB_SETTINGS']['db']
        db.get_connection().drop_database(current_db)

    def test_user_registration(self):
        res = self.test_client.post(
            'http://localhost:5000/register',
            json = USER
        )
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        reg_res = self.test_client.post(
            'http://localhost:5000/register',
            json = USER
        )
        login_res = self.test_client.post(
            'http://localhost:5000/login',
            json = USER
        )
        self.assertEqual(login_res.status_code, 302)
