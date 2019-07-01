from core import db

class User(db.Document):
    email = db.EmailField(
        required = True,
        unique = True
    )
    username = db.StringField(
        required = True,
        unique = True
    )
    password = db.StringField(
        required = True,
    )
    meta = {
        # set name of the collection
        'collection': 'users'
    }
