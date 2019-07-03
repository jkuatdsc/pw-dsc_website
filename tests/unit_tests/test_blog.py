from core import create_app, db
from unittest import TestCase

USER = {
    'email': 'jonnieey@gmail.com',
    'username': 'jonnieey',
    'password': 'password'
}
ARTICLE = {
    'title': 'Kuroko no basket',
    'description': 'Sports anime',
    'content' : 'This is the best sports anime',
}
BASE_URL = 'http://localhost:5000'

class ArticleTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

    def tearDown(self):
        current_db = self.app.config['MONGODB_SETTINGS']['db']
        db.get_connection().drop_database(current_db)
    
    def url_helper(self, url):
        return '%s/%s' % (BASE_URL, url)

    def register(self):
        res = self.test_client.post(
            self.url_helper('register'),
            json = USER
        )
        return res
    def login(self):
        res = self.test_client.post(
            self.url_helper('login'),
            json = USER
        )
        return res

    def test_user_can_create_article(self):
        self.register()
        refresh_token = self.login().json['refresh_token']

        res = self.test_client.post(
            self.url_helper('article'),
            headers = {'Authorization': f"Bearer {refresh_token}"},
            json = ARTICLE
        )
        self.assertEqual(res.status_code, 201)

    def test_user_can_create_article_without_content(self):
        self.register()
        refresh_token = self.login().json['refresh_token']

        cust_art = ARTICLE.copy()
        cust_art.pop('content')

        res = self.test_client.post(
            self.url_helper('article'),
            headers = {'Authorization': f"Bearer {refresh_token}"},
            json = cust_art
        )
        self.assertEqual(res.status_code, 400)
    
    def  test_create_article_without_login(self):
        res = self.test_client.post(
            self.url_helper('article')
        )
        self.assertEqual(res.status_code, 401)
    
