import os
from mongoengine import *
from flask import current_app

connect(db=os.getenv('DB'), host=os.getenv('HOST'), port=int(os.getenv('PORT')))

class BlogPost(Document):
    title = StringField(required=True, max_length=50)
    content = StringField(required=True)
    