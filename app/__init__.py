from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from instance.config import config
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
from time import strftime

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()

def flatten_error(item):
    result = []
    if isinstance(item, list):
        for i in item:
            result.extend(flatten_error(i))
    elif isinstance(item, dict):
        for key in item:
            result.extend(flatten_error(item[key]))
    else:
        result = [item]
    return result

def create_app(config_name):


    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    # Enable CORS
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        # This avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler.
        if response.status_code != 500:
            ts = strftime('[%Y-%b-%d %H:%M]')
            message = '{0} {1} {2} {3} {4} {5}'.format(
                          ts,
                          request.remote_addr,
                          request.method,
                          request.scheme,
                          request.full_path,
                          response.status)
            print(message)
        return response

    # All Exceptions
    @app.errorhandler(Exception)
    def general_error(error):
        messaged_errors = [400, 401, 403]
        status_code = 500
        if isinstance(error, HTTPException):
            status_code = error.code
        message = {}
        if status_code in messaged_errors:
            message = {'non_field_errors': flatten_error(error.description)}
        elif isinstance(error.description, str):
            message = {'message': error.description}
        else:
            message = error.description
        return message, status_code

    for ex in default_exceptions:
        app.register_error_handler(ex, general_error)

    # All blueprints

    # V1
    from app.api.v1.wallet.wallet_api import wallet_bp as wallet_v1
    from app.api.v1.user.user_api import init_bp as init_v1

    app.register_blueprint(wallet_v1)
    app.register_blueprint(init_v1)

    return app
