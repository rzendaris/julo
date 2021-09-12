"""
List of wallet models
"""
from app.models.base_models import TimeStampedModel
from app import db


class Wallet(TimeStampedModel):

    __tablename__ = 'wallet'

    owned_by = db.Column(db.ForeignKey('user_info.customer_xid'),
                         nullable=False, index=True)
    status = db.Column(db.String(256))
    last_update_status = db.Column(db.DateTime(timezone=True))
    balance = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))

    def __init__(self, owned_by, status, balance):
        self.owned_by = owned_by
        self.status = status
        self.balance = balance
