from flask import Flask

from flask_mongoengine import MongoEngine

from flask_restful import Api
from flask_jwt_extended import JWTManager

db = MongoEngine()

from .config import config
from accounts.views import Register, Login, RefreshAccessToken
from DSC_jkuat.views import CreateArticle, GetArticle, GetAllArticles

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app)
    
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(RefreshAccessToken, '/refresh-token')
    api.add_resource(CreateArticle, '/article')
    api.add_resource(GetArticle, '/articles/<string:article_id>')
    api.add_resource(GetAllArticles, '/articles')
    
    return app

