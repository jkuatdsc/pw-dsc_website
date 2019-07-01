from flask import Flask

from flask_mongoengine import MongoEngine

from flask_restful import Api
from flask_jwt_extended import JWTManager

db = MongoEngine()

from .config import config
from accounts.views import Register, Login

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app)
    
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    
    return app

