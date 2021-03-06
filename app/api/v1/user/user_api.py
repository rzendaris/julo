import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify
from marshmallow import ValidationError

from app.api.v1.user.user_request import InitUserRequestSchema
from app.constants.status_enum import ResponseEnum
from app.constants.wallet_status_enum import WalletStatusEnum
from app.models.user_models import UserInfo
from app.models.wallet_models import Wallet
from app.utils.response import response

init_bp = Blueprint("init_v1", __name__,
                    url_prefix='/api/v1/init/')


@init_bp.route('/', methods=['POST'])
def post_init():
    data = request.form or {}
    request_schema = InitUserRequestSchema()
    try:
        request_data = request_schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        error_return = {
            "error": err.messages
        }
        return response(ResponseEnum.FAIL.value, error_return, 400)

    customer_xid = data['customer_xid']
    user_exist = UserInfo.query.filter_by(customer_xid=customer_xid).first()
    if not user_exist:
        user_data = UserInfo(customer_xid)
        user_data.save()

        user_wallet = Wallet(customer_xid, WalletStatusEnum.DISABLED.value, 0)
        user_wallet.save()

    token = jwt.encode({
        'customer_xid': customer_xid,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config.get('JWT_SECRET_KEY'))

    payload = {
        'token': token.decode('utf-8')
    }
    return response(ResponseEnum.SUCCESS.value, payload, 201)
