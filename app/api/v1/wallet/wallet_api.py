from flask import Blueprint, request
from app.utils.response import response
from app.utils.authentication import Auth
from app.constants.status_enum import ResponseEnum

wallet_bp = Blueprint("wallet_v1", __name__,
                      url_prefix='/api/v1/wallet/')


@wallet_bp.route('init', methods=['POST'])
@Auth.token_required
def post_init():
    data = request.form or {}
    payload = {
        "name": data['customer_xid'],
        "wallet": 0
    }

    return response(ResponseEnum.SUCCESS.value, payload, 201)
