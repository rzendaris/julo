from app.constants.status_enum import ResponseEnum
from flask import jsonify


def response(status, data, http_code):
    payload = {
        "status": status
    }

    if status == ResponseEnum.ERROR.value:
        payload['message'] = data
    else:
        payload['data'] = data

    return jsonify(payload), http_code
