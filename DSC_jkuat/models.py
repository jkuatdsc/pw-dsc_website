from datetime import datetime

from core import db
from accounts.models import User

class Article(db.Document):
    """
    Model for article collection
    """
    title = db.StringField(
        required = True,
        max_length = 30
    )
    description = db.StringField(
        required = True,
        max_length = 80
    )
    author = db.ReferenceField(
        'User',
        required = True,
        # Nullify the relationship between article
        # and author when user is deleted
        reverse_delete_rule = db.NULLIFY
    )
    created = db.ComplexDateTimeField(
        default = datetime.utcnow()
    )
    # Implement to support images, and other media 
    content = db.StringField(
        required = True
    )
    ## others to implement
    # updated
    # ratings

    meta = {
        'collection': 'articles',
        'ordering': ['-created']
    }


    

