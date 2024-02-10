from marshmallow import Schema, fields, ValidationError

from backend.lib.lots import schema_lot_validator
from backend.exc import LotEndedError, LotDoesNotExist


class SignUpSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class SignInSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LotSchema(Schema):
    lot_name = fields.Str(required=True)
    description = fields.Str()
    end_date = fields.DateTime(required=True)


def lot_id_validator(value: int):
    try:
        schema_lot_validator(value)
    except (LotEndedError, LotDoesNotExist) as e:
        raise ValidationError(e.message)


def amount_validator(value: int):
    if value < 0:
        raise ValidationError("Invalid bet amount")


class BetCreationSchema(Schema):
    lot_id = fields.Int(required=True, validate=lot_id_validator)
    amount = fields.Int(required=True, validate=amount_validator)
