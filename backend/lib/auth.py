from flask import Response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
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
