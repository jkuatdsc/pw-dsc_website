from core import create_app, db
from unittest import TestCase

USER1 = {
    'email': 'jonnieey@gmail.com',
    'username': 'jonnieey',
    'password': 'password'
}
USER2 = {
    'email': 'anderson@gmail.com',
    'username': 'anderson',
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

    def register(self, user):
        res = self.test_client.post(
            self.url_helper('register'),
            json = user
        )
        return res
    def login(self, user):
        res = self.test_client.post(
            self.url_helper('login'),
            json = user
        )
        return res
    def create_article(self, login_res=None, article=None):
        headers = '' if not login_res else {
            'Authorization': 'Bearer %s' % (login_res.json['refresh_token'])
            }
        new_article = self.test_client.post(
            self.url_helper('article'),
            headers = headers,
            json = article
        )
        return new_article

    def test_user_can_create_article(self):
        self.register(USER1)
        login_res = self.login(USER1)

        res = self.create_article(login_res, ARTICLE)
        self.assertEqual(res.status_code, 201)

    def test_user_can_create_article_without_content(self):
        self.register(USER1)
        login_res = self.login(USER1)

        cust_art = ARTICLE.copy()
        cust_art.pop('content')

        res = self.create_article(login_res, cust_art)
        self.assertEqual(res.status_code, 400)
    
    def  test_create_article_without_login(self):
        res = self.create_article(article=ARTICLE) 
        self.assertEqual(res.status_code, 401)
    
    def test_get_article_by_id(self):
        self.register(USER1)
        login_res = self.login(USER1)

        new_article = self.create_article(login_res, ARTICLE)
        new_article_pk = new_article.json['article']['_id']['$oid']

        res = self.test_client.get(
            self.url_helper('articles/%s' % (new_article_pk))
        )
        self.assertEqual(res.status_code, 200)
    
    def test_get_all_articles(self):
        self.register(USER1)
        login_res = self.login(USER1)

        for article in range(0, 5):
            self.create_article(login_res, ARTICLE)

        res = self.test_client.get(
            self.url_helper('articles')
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['articles']), 5)
    
    def test_get_user_articles(self):
        user1 = self.register(USER1)
        user2 = self.register(USER2)

        login_res_1 = self.login(USER1)
        login_res_2 = self.login(USER2)

        for user in USER1, USER2:
            if user ==  USER1:
                login_res = login_res_1
            else:
                login_res = login_res_2

            for article in range(3):
                self.create_article(login_res, ARTICLE)

        res = self.test_client.get(
            self.url_helper('/users/anderson/articles')
        )
        self.assertEqual(res.status_code, 200)

