from flask import Flask
from flask_restful import Api
from instance.config import app_config

from .views.blog_post import BlogPostView

def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    api.add_resource(BlogPostView, "/api/blogs")
    return app