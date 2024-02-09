from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from functools import partial

from marshmallow import Schema, fields, ValidationError

from backend.utils import get_from_env_or_file, read_yaml, get_env_asserted


PROJECT_PATH = Path(__file__).parent.parent


@dataclass(slots=True, frozen=True)
class Config:
    DEBUG: bool
    SQLALCHEMY_DATABASE_URI: str
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: list[str]
    SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: timedelta
    AWS_S3_DOMAIN: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str


class ConfigSchema(Schema):
    debug = fields.Bool(required=True)
    sqlalchemy_database_uri = fields.Str(required=True)
    jwt_secret_key = fields.Str(required=True)
    secret_key = fields.Str(required=True)
    jwt_access_token_expires = fields.Int(required=True)  # days
    aws_s3_domain = fields.Str(required=True)
    aws_access_key_id = fields.Str(required=True)
    aws_secret_access_key = fields.Str(required=True)


_config = None


def parse_config() -> Config:
    config_path = PROJECT_PATH / get_env_asserted("BACKEND_CONFIG_PATH")
    settings_from_file = read_yaml(config_path)
    option_getter = partial(get_from_env_or_file, file=settings_from_file)

    try:
        config_validated = ConfigSchema().load(
            dict(
                debug=option_getter("debug"),
                sqlalchemy_database_uri=option_getter("sqlalchemy_database_uri"),
                jwt_secret_key=option_getter("jwt_secret_key"),
                secret_key=option_getter("secret_key"),
                jwt_access_token_expires=option_getter("jwt_access_token_expires"),
                aws_s3_domain=option_getter("aws_s3_domain"),
                aws_access_key_id=get_env_asserted("aws_access_key_id"),
                aws_secret_access_key=get_env_asserted("aws_secret_access_key"),
            )
        )
    except ValidationError as e:
        raise RuntimeError("Configuration failed") from e

    config = Config(
        DEBUG=config_validated["debug"],
        SQLALCHEMY_DATABASE_URI=config_validated["sqlalchemy_database_uri"],
        JWT_SECRET_KEY=config_validated["jwt_secret_key"],
        JWT_TOKEN_LOCATION=["headers"],
        SECRET_KEY=config_validated["secret_key"],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(
            days=config_validated["jwt_access_token_expires"]
        ),
        AWS_S3_DOMAIN=config_validated["aws_s3_domain"],
        AWS_ACCESS_KEY_ID=config_validated["aws_access_key_id"],
        AWS_SECRET_ACCESS_KEY=config_validated["aws_secret_access_key"],
    )

    return config


def get_config() -> Config:
    global _config

    if _config is None:
        _config = parse_config()
    return _config
