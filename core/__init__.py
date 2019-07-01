from flask import Flask

from flask_mongoengine import MongoEngine

from flask_restful import Api

db = MongoEngine()

from .config import config
from accounts.views import Register

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    
    api = Api(app)
    
    api.add_resource(Register, '/register')
    

    return app

