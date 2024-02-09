from typing import cast

from flask import Blueprint, request, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt

from backend.exc import UserAlreadyExist
from backend.lib.schemas import SignUpSchema, SignInSchema
from backend.types import SignInPayload, SignUpPayload
from backend.lib.auth import (
    create_user,
    authenticate_user,
    AuthenticationError,
    UserDoesNotExist,
    revoke_token,
)
from backend.utils import success_response, error_response


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.route("/sign_up", methods=("POST",))
def sign_up():
    """
    ---
    post:
        summary: sign up
        requestBody:
            content:
              application/json:
                schema:
                  SignUpSchema
        responses:
            '200':
                content:
                    application/json:
                        schema: AuthSuccessResponse
            '400':
                content:
                    application/json:
                        schema: SignUpErrorResponse
            '409':
                content:
                    application/json:
                        schema: ErrorMessageResponse
        tags:
        - auth
    """
    try:
        request_data = cast(
            SignUpPayload,
            SignUpSchema().load(request.get_json()),
        )
    except ValidationError as e:
        return error_response(status_code=400, errors=e.messages)

    try:
        user = create_user(request_data)
    except UserAlreadyExist:
        current_app.logger.warning(f"User({request_data['email']}) already exists")
        return error_response(
            status_code=409, errors={"message": "User already exists"}
        )

    access_token = create_access_token(identity=user)
    return success_response(
        data={"access_token": access_token, "user_id": user.id},
    )


@bp.route("/sign_in", methods=("POST",))
def sign_in():
    """
    ---
    post:
        summary: sign in
        requestBody:
            content:
              application/json:
                schema:
                  SignInSchema
        responses:
            '200':
                content:
                    application/json:
                        schema: AuthSuccessResponse
            '400':
                content:
                    application/json:
                        schema: SignInErrorResponse
            '401':
                content:
                    application/json:
                        schema: ErrorMessageResponse
        tags:
        - auth
    """
    try:
        request_data = cast(
            SignInPayload,
            SignInSchema().load(request.get_json()),
        )
    except ValidationError as e:
        return error_response(status_code=400, errors=e.messages)

    try:
        user = authenticate_user(
            email=request_data["email"],
            password=request_data["password"],
        )
    except AuthenticationError:
        current_app.logger.warning(f"Ivalid password")
        return error_response(
            status_code=401,
            errors={"message": "Unauthorized"},
        )
    except UserDoesNotExist:
        current_app.logger.warning(f"No such user: {request_data['email']}")
        return error_response(
            status_code=401,
            errors={"message": "User not found"},
        )

    access_token = create_access_token(identity=user)
    return success_response(
        data={"access_token": access_token, "user_id": user.id},
    )


@bp.route("/logout", methods=("POST",))
@jwt_required()
def logout():
    """
    ---
    post:
        summary: logout
        responses:
            '200':
                description: Успішно
            '401':
                description: Користувач не авторизований
        tags:
        - auth
    """
    jti = get_jwt()["jti"]
    revoke_token(jti=jti)

    return success_response(
        data={"message": "JWT successfully revoked"},
    )
