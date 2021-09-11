import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify

from app.constants.status_enum import ResponseEnum
from app.constants.wallet_status_enum import WalletStatusEnum
from app.models.user_models import UserInfo
from app.utils.response import response

init_bp = Blueprint("init_v1", __name__,
                    url_prefix='/api/v1/init/')


@init_bp.route('/', methods=['POST'])
def post_init():
    data = request.form or {}
    customer_xid = data['customer_xid']
    user_exist = UserInfo.query.filter_by(owned_by=customer_xid).first()
    if not user_exist:
        user_data = UserInfo(customer_xid, WalletStatusEnum.DISABLED.value, 0)
        user_data.save()

    token = jwt.encode({
        'user_id': customer_xid,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config.get('JWT_SECRET_KEY'))

    payload = {
        'token': token.decode('utf-8')
    }
    return response(ResponseEnum.SUCCESS.value, payload, 201)
