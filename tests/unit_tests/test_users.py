from unittest import TestCase

from apps.core import create_app, db

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
    
    """
    Register and login helpers
    """
    def register(self):
        res = self.test_client.post(
            'http://localhost:5000/register',
            json = USER
        )
        return res

    def login(self):
        res = self.test_client.post(
            'http://localhost:5000/login',
            json = USER
        )
        return res

   
    def test_user_registration(self):
        res = self.register() 
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        reg_res = self.register()
        login_res = self.login() 
        self.assertEqual(login_res.status_code, 302)

    def test_get_fresh_token_from_logged_in_user(self):
        reg_res = self.register()
        login_res = self.login()

        refresh_token = login_res.json['refresh_token']
        headers = {'Authorization': f"Bearer {refresh_token}" }

        ref_tok = self.test_client.post(
            'http://localhost:5000/refresh-token',
            headers = headers
        )
        self.assertTrue(ref_tok.json['new_access_token'])

        
