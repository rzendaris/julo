"""
List of user models
"""
from app.models.base_models import TimeStampedModel
from app import db


class UserInfo(TimeStampedModel):

    __tablename__ = 'user_info'

    owned_by = db.Column(db.String(256))
    status = db.Column(db.String(256))
    last_update_status = db.Column(db.DateTime(timezone=True))
    balance = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))

    def __init__(self, owned_by, status, balance):
        self.owned_by = owned_by
        self.status = status
        self.balance = balance

    def __str__(self):
        return '{0}'.format(self.owned_by)
