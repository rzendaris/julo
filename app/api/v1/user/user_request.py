from app import ma
from marshmallow import fields, validate,  ValidationError, validates_schema


class InitUserRequestSchema(ma.Schema):
    customer_xid = fields.String(required=True)