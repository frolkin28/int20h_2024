from typing import cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import unset_jwt_cookies, jwt_required

from backend.lib.schemas import SignUpSchema, SignInSchema
from backend.types import SignInPayload, SignUpPayload
from backend.lib.auth import (
    create_user,
    authenticate_user,
    set_tokens_cookies,
    AuthenticationError,
    UserDoesNotExist,
)


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/sign_up", methods=("POST",))
def sign_up():
    try:
        request_data = cast(
            SignUpPayload,
            SignUpSchema().load(request.get_json()),
        )
    except ValidationError as e:
        return jsonify({"errors": e.messages})

    user_id = create_user(request_data)
    response = jsonify({"user_id": user_id})
    set_tokens_cookies(response, user_id)
    return response


@bp.route("/sign_in", methods=("POST",))
def sign_in():
    try:
        request_data = cast(
            SignInPayload,
            SignInSchema().load(request.get_json()),
        )
    except ValidationError as e:
        return jsonify({"errors": e.messages})

    try:
        user_id = authenticate_user(
            login=request_data["login"],
            password=request_data["password"],
        )
    except AuthenticationError:
        return jsonify({"message": "Unauthorized"}), 401
    except UserDoesNotExist:
        return jsonify({"message": "User not found"}), 401

    response = jsonify({"user_id": user_id})
    set_tokens_cookies(response, user_id)
    return response


@bp.route("/logout", methods=("POST",))
@jwt_required()
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response
