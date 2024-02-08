from datetime import datetime

from flask_jwt_extended import JWTManager, decode_token
from jwt import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from backend.exc import (
    UserAlreadyExist,
    UserDoesNotExist,
    AuthenticationError,
)
from backend.models import TokenBlocklist, User
from backend.types import SignInPayload
from backend.services.db import db


jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    return user.id


def get_user_by_identity(identity: int) -> User | None:
    return User.query.filter(User.id == identity).one_or_none()


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data: dict):
    identity = jwt_data["sub"]
    return get_user_by_identity(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = (
        db.session.query(TokenBlocklist.id).filter(TokenBlocklist.jti == jti).scalar()
    )

    return token is not None


def create_user(payload: SignInPayload) -> User:
    user = User(
        email=payload["email"],
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        password=generate_password_hash(payload["password"]),
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        raise UserAlreadyExist from e

    return user


def authenticate_user(email: str, password: str) -> User:
    user = (
        User.query.with_entities(
            User.id,
            User.password,
        )
        .filter(User.email == email)
        .one_or_none()
    )
    if user is None:
        raise UserDoesNotExist
    if not check_password_hash(user.password, password):
        raise AuthenticationError
    return user


def revoke_token(jti: str):
    now = datetime.now()
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()


def verify_user_token(token: str | None) -> User | None:
    if not token:
        return None
    try:
        jwt_data = decode_token(token)
    except ExpiredSignatureError:
        return None

    identity = jwt_data["sub"]
    return get_user_by_identity(identity)
