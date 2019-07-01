from flask import Flask

from flask_mongoengine import MongoEngine

from .config import config

db = MongoEngine()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return app

