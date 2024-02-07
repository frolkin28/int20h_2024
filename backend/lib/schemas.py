from marshmallow import Schema, fields


class SignUpSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponse(Schema):
    user_id = fields.Int(required=True)


class ErrorMessageResponse(Schema):
    message = fields.Str(required=True)


class SignInSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class AddLotSchema(Schema):
    lot_name = fields.Str(required=True)
    description = fields.Str()
    end_date = fields.DateTime(required=True)

class LotResponse(Schema):
    lot_id = fields.Int(required=True)


