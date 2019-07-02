from core import create_app, db
from unittest import TestCase

USER = {
    'email': 'jonnieey@gmail.com',
    'username': 'jonnieey',
    'password': 'password'
}

class ArticleTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        current_db = self.app.config['MONGODB_SETTINGS']['db']
        db.get_connection().drop_database(current_db)
    
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

    def test_user_can_create_article(self):
        self.register()
        refresh_token = self.login().json['refresh_token']

        res = self.test_client.post(
            'http://localhost:5000/article',
            headers = {'Authorization': f"Bearer {refresh_token}"},
            json = {
                'title': 'Kuroko no basket',
                'description': 'Sports anime',
                'content' : 'This is the best sports anime',
            }
        )
        self.assertEqual(res.status_code, 201)
