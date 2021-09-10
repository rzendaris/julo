"""
List of user models
"""
from app.models.base_models import TimeStampedModel
from sqlalchemy.orm import backref
from app import db

class UserInfo(TimeStampedModel):

    __tablename__ = 'user_info'

    username = db.Column(db.String(256))
    name = db.Column(db.String(256))

    def __init__(self, id, username, name):
        self.id = id
        self.username = username
        self.name = name

    def __str__(self):
        return '{0}-{1}'.format(self.id, self.username)