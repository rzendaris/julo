from flask import Flask, request, current_app
import jwt
from functools import wraps

from app.constants.status_enum import ResponseEnum
from app.utils.response import response


class Auth:

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            authorization_header = None
            if 'Authorization' in request.headers:
                authorization_header = request.headers['Authorization']
            if not authorization_header:
                return response(ResponseEnum.ERROR.value, 'Unauthorized Access!', 401)

            try:
                token = authorization_header.split(" ")
                data = jwt.decode(token[1], current_app.config.get('JWT_SECRET_KEY'))
                if not data:
                    return response(ResponseEnum.ERROR.value, 'Unauthorized Access!', 401)
            except:
                return response(ResponseEnum.ERROR.value, 'Unauthorized Access!', 401)
            return f(*args, **kwargs)

        return decorated
