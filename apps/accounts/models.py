from flask_bcrypt import Bcrypt

from apps.core import db

mycrypt = Bcrypt()

class User(db.Document):
    email = db.EmailField(
        required = True,
        unique = True
    )
    username = db.StringField(
        required = True,
        unique = True
    )
    password_hash = db.StringField(
        required = True,
    )
    meta = {
        # set name of the collection
        'collection': 'users'
    }
    """
    call to user's object password attribute will raise AttributeError
    """
    @property
    def password(self):
        raise AttributeError('password attribute is not readable')
    """
    when user password property is assigned, set it to a hashed string
    """    
    @password.setter
    def password(self, password):
        self.password_hash = mycrypt.generate_password_hash(
            password).decode()

    @staticmethod
    def verify_password(hash, password):
        return mycrypt.check_password_hash(hash, password)
