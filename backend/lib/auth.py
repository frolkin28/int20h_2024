from functools import wraps
import typing as t

from flask import Response, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from backend.exc import (
    UserAlreadyExist,
    UserDoesNotExist,
    AuthenticationError,
)
from backend.models import User
from backend.types import SignInPayload
from backend.services.db import db


def create_user(payload: SignInPayload) -> int:
    user = User(
        login=payload["login"],
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        password=generate_password_hash(payload["password"]),
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        raise UserAlreadyExist from e

    return user.id


def authenticate_user(login: str, password: str) -> int:
    user = db.session.query(User.id, User.password).filter(User.login == login).first()
    if user is None:
        raise UserDoesNotExist
    if not check_password_hash(user.password, password):
        raise AuthenticationError
    return user.id


def set_tokens_cookies(response: Response, user_id: int):
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)


def get_user_by_id(user_id: int) -> User:
    return db.session.query(User).get(user_id)


TReturn = t.TypeVar("TReturn")
TFunc = t.Callable[..., TReturn]
TFuncWithUser = t.Callable[t.Concatenate[User, ...], TReturn]


def login_required(func: TFunc) -> TFunc:
    @wraps(func)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> TReturn:
        try:
            if not verify_jwt_in_request():
                return jsonify({}), 401
        except NoAuthorizationError:
            return jsonify({}), 401

        user_id = get_jwt_identity()
        if not get_user_by_id(user_id):
            return jsonify({}), 401

        return func(*args, **kwargs)

    return t.cast(TFunc, wrapper)


def with_auth_user(func: TFunc) -> TFuncWithUser:
    @wraps(func)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> TReturn:
        try:
            if not verify_jwt_in_request():
                return jsonify({}), 401
        except NoAuthorizationError:
            return jsonify({}), 401

        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({}), 401

        return func(user, *args, **kwargs)

    return t.cast(TFuncWithUser, wrapper)
