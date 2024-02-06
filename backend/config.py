from dataclasses import dataclass
from pathlib import Path

from backend.utils import get_env, read_yaml


PROJECT_PATH = Path(__file__).parent.parent


@dataclass(slots=True, frozen=True)
class Config:
    DEBUG: bool
    SQLALCHEMY_DATABASE_URI: str
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: list[str]
    SECRET_KEY: str
    JWT_COOKIE_SECURE: bool = True


def get_config() -> Config:
    config_path = PROJECT_PATH / get_env("BACKEND_CONFIG_PATH")
    settings_from_file = read_yaml(config_path)
    try:
        config = Config(
            DEBUG=settings_from_file["debug"],
            SQLALCHEMY_DATABASE_URI=settings_from_file["db_uri"],
            JWT_SECRET_KEY="123124324324234",
            JWT_TOKEN_LOCATION=["cookies"],
            SECRET_KEY="QER2#$%&%&**@egrhtjk",
        )
    except KeyError as e:
        raise RuntimeError("Invalid config format") from e
    return config
