from logging import getLogger
from typing import cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import unset_jwt_cookies, jwt_required

from backend.exc import UserAlreadyExist
from backend.lib.schemas import SignUpSchema, SignInSchema
from backend.types import SignInPayload, SignUpPayload
from backend.lib.auth import (
    create_user,
    authenticate_user,
    set_tokens_cookies,
    AuthenticationError,
    UserDoesNotExist,
)

log = getLogger(__name__)

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
        user_id = create_user(request_data)
    except UserAlreadyExist:
        log.warning(f"User({request_data['login']}) already exists")
        return jsonify({"message": "User already exists"}), 409

    response = jsonify({"user_id": user_id})
    set_tokens_cookies(response, user_id)
    return response


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
        user_id = authenticate_user(
            login=request_data["login"],
            password=request_data["password"],
        )
    except AuthenticationError:
        log.warning(f"Ivalid password")
        return jsonify({"message": "Unauthorized"}), 401
    except UserDoesNotExist:
        log.warning(f"No such user: {request_data['login']}")
        return jsonify({"message": "User not found"}), 401

    response = jsonify({"user_id": user_id})
    set_tokens_cookies(response, user_id)
    return response


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
    response = jsonify()
    unset_jwt_cookies(response)
    return response
