
from app.constants.status_enum import ResponseEnum


def response(status, data, http_code):
    payload = {
        "status": status
    }

    if status == ResponseEnum.ERROR.value:
        payload['message'] = data
    else:
        payload['data'] = data

    return payload, http_code