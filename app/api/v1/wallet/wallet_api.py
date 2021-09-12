from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime

from app.api.v1.wallet.wallet_request import DepositRequestSchema, WithdrawalRequestSchema
from app.api.v1.wallet.wallet_serializer import WalletSchema, DepositSchema, WithdrawalSchema
from app.models.wallet_models import Wallet
from app.models.deposit_models import Deposit
from app.models.withdrawal_models import Withdrawal
from app.utils.response import response
from app.utils.authentication import Auth
from app.constants.status_enum import ResponseEnum
from app.constants.wallet_status_enum import WalletStatusEnum, DepositStatusEnum

wallet_bp = Blueprint("wallet_v1", __name__,
                      url_prefix='/api/v1/wallet')


@wallet_bp.route('', methods=['GET'])
@Auth.token_required
def get_wallet():
    user_wallet = Wallet.query.filter_by(owned_by=get_wallet.customer_xid).first()
    if user_wallet.status == WalletStatusEnum.DISABLED.value:
        return response(ResponseEnum.FAIL.value, {'error': 'Disabled'}, 404)

    schema = {
        'wallet': WalletSchema(exclude=('disabled_at',)).dump(user_wallet)
    }
    return response(ResponseEnum.SUCCESS.value, schema, 200)


@wallet_bp.route('', methods=['POST'])
@Auth.token_required
def enable_wallet():
    user_wallet = Wallet.query.filter_by(owned_by=enable_wallet.customer_xid).first()
    if user_wallet.status == WalletStatusEnum.ENABLED.value:
        return response(ResponseEnum.FAIL.value, {'error': 'Already Enabled'}, 400)

    user_wallet.status = WalletStatusEnum.ENABLED.value
    user_wallet.last_update_status = datetime.utcnow()
    user_wallet.save()

    schema = {
        'wallet': WalletSchema(exclude=('disabled_at',)).dump(user_wallet)
    }

    return response(ResponseEnum.SUCCESS.value, schema, 201)


@wallet_bp.route('', methods=['PATCH'])
@Auth.token_required
def disable_wallet():
    data = request.form or {}
    is_disabled = data['is_disabled']
    user_wallet = Wallet.query.filter_by(owned_by=disable_wallet.customer_xid).first()
    if is_disabled and user_wallet.status == WalletStatusEnum.DISABLED.value:
        return response(ResponseEnum.FAIL.value, {'error': 'Already Disabled'}, 400)

    user_wallet.status = WalletStatusEnum.DISABLED.value
    user_wallet.last_update_status = datetime.utcnow()
    user_wallet.save()

    schema = {
        'wallet': WalletSchema(exclude=('enabled_at',)).dump(user_wallet)
    }

    return response(ResponseEnum.SUCCESS.value, schema, 200)


@wallet_bp.route('deposits', methods=['POST'])
@Auth.token_required
def deposit_wallet():
    data = request.form or {}

    # Validation area
    user_wallet = Wallet.query.filter_by(owned_by=deposit_wallet.customer_xid).first()
    if user_wallet.status == WalletStatusEnum.DISABLED.value:
        return response(ResponseEnum.FAIL.value, {'error': 'Disabled'}, 404)

    request_schema = DepositRequestSchema()
    try:
        request_data = request_schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return response(ResponseEnum.FAIL.value, err.messages, 400)

    deposit = Deposit(deposit_wallet.customer_xid, DepositStatusEnum.SUCCESS.value, request_data['amount'], request_data['reference_id'])
    deposit.save()

    if deposit:
        user_wallet.balance += deposit.amount
        user_wallet.save()

    schema = {
        'deposit': DepositSchema().dump(deposit)
    }

    return response(ResponseEnum.SUCCESS.value, schema, 201)


@wallet_bp.route('withdrawals', methods=['POST'])
@Auth.token_required
def withdrawal_wallet():
    data = request.form or {}

    # Validation area
    user_wallet = Wallet.query.filter_by(owned_by=withdrawal_wallet.customer_xid).first()
    if user_wallet.status == WalletStatusEnum.DISABLED.value:
        return response(ResponseEnum.FAIL.value, {'error': 'Disabled'}, 404)

    request_schema = WithdrawalRequestSchema(context={'customer_xid': withdrawal_wallet.customer_xid})
    try:
        request_data = request_schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return response(ResponseEnum.FAIL.value, err.messages, 400)

    withdrawal = Withdrawal(withdrawal_wallet.customer_xid, DepositStatusEnum.SUCCESS.value, request_data['amount'], request_data['reference_id'])
    withdrawal.save()

    if withdrawal:
        user_wallet.balance -= withdrawal.amount
        user_wallet.save()

    schema = {
        'withdrawal': WithdrawalSchema().dump(withdrawal)
    }

    return response(ResponseEnum.SUCCESS.value, schema, 201)
