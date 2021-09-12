from app import ma
from app.models.deposit_models import Deposit
from app.models.wallet_models import Wallet
from marshmallow import fields, validates_schema, ValidationError

from app.models.withdrawal_models import Withdrawal


class WalletSchema(ma.ModelSchema):
    enabled_at = fields.Method('get_enabled_at')
    disabled_at = fields.Method('get_disabled_at')

    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'enabled_at', 'disabled_at', 'balance', 'status')

    def get_enabled_at(self, obj):
        return obj.last_update_status

    def get_disabled_at(self, obj):
        return obj.last_update_status


class DepositSchema(ma.ModelSchema):
    deposited_at = fields.Method('get_deposited_at')

    class Meta:
        model = Deposit
        fields = ('id', 'deposited_by', 'status', 'deposited_at', 'amount', 'reference_id')

    def get_deposited_at(self, obj):
        return obj.created_at


class WithdrawalSchema(ma.ModelSchema):
    withdrawn_at = fields.Method('get_withdrawn_at')

    class Meta:
        model = Withdrawal
        fields = ('id', 'withdrawn_by', 'status', 'withdrawn_at', 'amount', 'reference_id')

    def get_withdrawn_at(self, obj):
        return obj.created_at
