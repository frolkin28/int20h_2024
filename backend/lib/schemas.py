from marshmallow import Schema, fields


class SignUpSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponse(Schema):
    user_id = fields.Int(required=True)


class ErrorMessageResponse(Schema):
    user_id = fields.Int(required=True)


class SignInSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)
