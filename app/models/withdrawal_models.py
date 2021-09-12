"""
List of wallet models
"""
from app.models.base_models import TimeStampedModel
from app import db


class Withdrawal(TimeStampedModel):

    __tablename__ = 'withdrawal'

    withdrawn_by = db.Column(db.ForeignKey('user_info.customer_xid'),
                             nullable=False, index=True)
    status = db.Column(db.String(256))
    reference_id = db.Column(db.String(256))
    amount = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))

    def __init__(self, withdrawn_by, status, amount, reference_id):
        self.withdrawn_by = withdrawn_by
        self.status = status
        self.amount = amount
        self.reference_id = reference_id
