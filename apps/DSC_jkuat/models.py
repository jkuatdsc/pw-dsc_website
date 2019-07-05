from datetime import datetime

from apps.core import db
from apps.accounts.models import User

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


class Comment(db.Document):
    """
    Model for comment collection 
    """
    article = db.ReferenceField(
        'Article',
        required = True,
        reverse_delete_rule = db.CASCADE
    )
    author = db.ReferenceField(
        'User',
        required = True,
        reverse_delete_rule = db.NULLIFY
    )
    created = db.ComplexDateTimeField(
        default = datetime.utcnow()
    )
    content = db.StringField(
        required = True
    )

    meta = {
        'collection': 'comments',
        'ordering': ['-created']
    }


