"""
List of user models
"""
from app.models.base_models import TimeStampedModel
from app import db


class UserInfo(TimeStampedModel):

    __tablename__ = 'user_info'

    customer_xid = db.Column(db.String(256), unique=True, index=True)

    def __init__(self, customer_xid):
        self.customer_xid = customer_xid

    def __str__(self):
        return '{0}'.format(self.customer_xid)
