from app import ma
from marshmallow import fields, validate,  ValidationError, validates_schema

from app.models.deposit_models import Deposit
from app.models.wallet_models import Wallet
from app.models.withdrawal_models import Withdrawal


class WithdrawalRequestSchema(ma.Schema):
    amount = fields.Integer(required=True)
    reference_id = fields.String(required=True)

    @validates_schema
    def validate_reference_id(self, data, **kwargs):
        errors = {}
        reference_id_exist = Withdrawal.query.filter_by(reference_id=data['reference_id']).first()
        if reference_id_exist:
            errors["reference_id"] = ["must be unique."]

        if errors:
            raise ValidationError(errors)

    @validates_schema
    def validate_amount(self, data, **kwargs):
        errors = {}
        if data['amount'] <= 0:
            errors["amount"] = ["Value must be greater than 0."]

        user_wallet = Wallet.query.filter_by(owned_by=self.context['customer_xid']).first()
        if data['amount'] > user_wallet.balance:
            errors["amount"] = ["Over than balance."]

        if errors:
            raise ValidationError(errors)


class DepositRequestSchema(ma.Schema):
    amount = fields.Integer(required=True, validate=validate.Range(min=1, error="Value must be greater than 0"))
    reference_id = fields.String(required=True)

    @validates_schema
    def validate_reference_id(self, data, **kwargs):
        errors = {}
        reference_id_exist = Deposit.query.filter_by(reference_id=data['reference_id']).first()
        if reference_id_exist:
            errors["reference_id"] = ["must be unique."]

        if errors:
            raise ValidationError(errors)
