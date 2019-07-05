from unittest import TestCase

from apps.core import create_app, db

USER = {
    'email': 'jonnieey@gmail.com',
    'username': 'jonnieey',
    'password': 'password'
}
ARTICLE = {
    'title': 'One piece',
    'description': 'Action anime',
    'content': 'This is teh best anime ever'
}
COMMENT = {
    'content': 'This is a test comment'
}

BASE_URL = 'http://localhost:5000'

class CommentTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.app = create_app(config_name='testing')
        self.test_client = self.app.test_client()

        self.register(USER)
        self.refresh_token = self.login(USER).json['refresh_token']
        self.test_article = self.test_client.post(
            self.url_helper('article'),
            headers = {'Authorization': 'Bearer %s' % (self.refresh_token)},
            json = ARTICLE
        )

    @classmethod
    def tearDownClass(self):
        current_db = self.app.config['MONGODB_SETTINGS']['db']
        db.get_connection().drop_database(current_db)
    
    @classmethod
    def url_helper(self, url):
        return '%s/%s' % (BASE_URL, url)

    @classmethod
    def register(self, user):
        reg_res = self.test_client.post(
            self.url_helper('register'),
            json = user
        )
        return reg_res

    @classmethod
    def login(self, user):
        login_res = self.test_client.post(
            self.url_helper('login'),
            json = user
        )
        return login_res

    def test_create_comment(self):
        article_id = self.test_article.json['article']['_id']['$oid']
        headers = {'Authorization': 'Bearer %s' % (self.refresh_token)}

        res = self.test_client.post(
            self.url_helper('/articles/%s/comment'% (article_id)),
            headers = headers,
            json = COMMENT
        )
        self.assertEqual(res.status_code, 201)
