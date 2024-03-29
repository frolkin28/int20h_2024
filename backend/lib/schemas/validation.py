from marshmallow import Schema, fields, ValidationError, validate

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


class LotCreationSchema(Schema):
    lot_name = fields.Str(required=True)
    description = fields.Str()
    end_date = fields.DateTime(required=True)
    start_price = fields.Float()


class FullLotSchema(Schema):
    lot_name = fields.Str(required=True)
    description = fields.Str()
    start_price = fields.Float()
    is_author = fields.Bool(required=True)
    author = {
        "email": fields.Str(required=True),
        "first_name": fields.Str(required=True),
        "last_name": fields.DateTime(required=True),
    }
    creation_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    pictures = fields.List(fields.Str())


class ListLotSchema(Schema):
    lot_name = fields.Str(required=True)
    lot_id = fields.Int(required=True)
    end_date = fields.DateTime(required=True)
    picture = fields.Str()
    price = fields.Float()


def lot_id_validator(value: int):
    try:
        schema_lot_validator(value)
    except (LotEndedError, LotDoesNotExist) as e:
        raise ValidationError(e.message)


class BetCreationSchema(Schema):
    lot_id = fields.Int(required=True, validate=lot_id_validator)
    amount = fields.Decimal(
        required=True,
        validate=[
            validate.Range(min=0, error="Ставка не може бути менше 0"),
        ],
        places=2,
    )
