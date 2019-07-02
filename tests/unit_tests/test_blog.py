from core import create_app
from unittest import TestCase

class ArticleTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        current_db = self.app.config['MONGODB_SETTINGS']['db']
        db.get_connection().drop_database(current_db)
    
    def test_user_can_create_article(self):
        res = self.test_client.post(
            'http://localhost:5000/article',
            json = {
                'title': 'Kuroko no basket',
                'description': 'Sports anime',
                'content' : 'This is the best sports anime',
            }
        )
        self.assertEqual(res.status_code, 201)
