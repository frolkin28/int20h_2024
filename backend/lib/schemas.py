from marshmallow import Schema, fields, ValidationError

from backend.lib.lots import lot_exists, schema_lot_validator
from backend.exc import LotEndedError, LotDoesNotExist


class SignUpSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponse(Schema):
    user_id = fields.Int(required=True)
    access_token = fields.Str(required=True)


class ErrorMessageResponse(Schema):
    message = fields.Str(required=True)


class SignInSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AddLotSchema(Schema):
    lot_name = fields.Str(required=True)
    description = fields.Str()
    end_date = fields.DateTime(required=True)


class LotResponse(Schema):
    lot_id = fields.Int(required=True)


class CustomDateTimeField(fields.Field):
    def _serialize(self, value, *args, **kwargs) -> str | None:
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


class BetResponseSchema(Schema):
    id = fields.Int(required=True)
    amount = fields.Int(required=True)
    creation_date = CustomDateTimeField(
        attribute="creation_date",
        required=True,
    )


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
