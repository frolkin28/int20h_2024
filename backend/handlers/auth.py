from typing import cast

from flask import Blueprint, jsonify, request, current_app
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
                        schema: AuthResponse
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
        return jsonify({"errors": e.messages}), 400

    try:
        user = create_user(request_data)
    except UserAlreadyExist:
        current_app.logger.warning(f"User({request_data['email']}) already exists")
        return jsonify({"message": "User already exists"}), 409

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token, user_id=user.id)


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
                        schema: AuthResponse
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
        return jsonify({"errors": e.messages}), 400

    try:
        user = authenticate_user(
            email=request_data["email"],
            password=request_data["password"],
        )
    except AuthenticationError:
        current_app.logger.warning(f"Ivalid password")
        return jsonify({"message": "Unauthorized"}), 401
    except UserDoesNotExist:
        current_app.logger.warning(f"No such user: {request_data['email']}")
        return jsonify({"message": "User not found"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token, user_id=user.id)


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
    from flask_jwt_extended import current_user

    current_app.logger.info(f"User: {current_user}")

    jti = get_jwt()["jti"]
    revoke_token(jti=jti)
    return jsonify(message="JWT successfully revoked")
