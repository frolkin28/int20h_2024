from marshmallow import Schema, fields

from backend.lib.schemas.validation import (
    SignUpSchema,
    SignInSchema,
    LotSchema,
)


def errors_field(schema: Schema) -> fields.Nested:
    fields_names: tuple[str, ...] = tuple(schema().fields.keys())

    return fields.Nested(
        Schema.from_dict(
            {field: fields.Str() for field in fields_names},
        ),
        allow_none=True,
    )


class ResponseSchema(Schema):
    success = fields.Bool(required=True)


class UserTokenSchema(Schema):
    user_id = fields.Int(required=True)
    access_token = fields.Str(required=True)


class AuthSuccessResponse(ResponseSchema):
    data = fields.Nested(UserTokenSchema)


class SignInErrorResponse(ResponseSchema):
    errors = errors_field(SignInSchema)


class SignUpErrorResponse(ResponseSchema):
    errors = errors_field(SignUpSchema)


class ErrorMessageSchema(Schema):
    message = fields.Str(required=True)


class ErrorMessageResponse(ResponseSchema):
    errors = fields.Nested(ErrorMessageSchema)


class LotIdSchema(Schema):
    lot_id = fields.Int(required=True)


class UpsertLotSuccessResponse(ResponseSchema):
    data = fields.Nested(LotIdSchema)


class UpsertLotErrorResponse(ResponseSchema):
    errors = errors_field(LotSchema)
