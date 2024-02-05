from dataclasses import dataclass
from pathlib import Path

from backend.utils import get_env, read_yaml


PROJECT_PATH = Path(__file__).parent.parent


@dataclass(slots=True, frozen=True)
class Config:
    DEBUG: bool
    SQLALCHEMY_DATABASE_URI: str


def get_config() -> Config:
    config_path = PROJECT_PATH / get_env("BACKEND_CONFIG_PATH")
    settings_from_file = read_yaml(config_path)
    try:
        config = Config(
            DEBUG=settings_from_file["debug"],
            SQLALCHEMY_DATABASE_URI=settings_from_file["db_uri"],
        )
    except KeyError as e:
        raise RuntimeError("Invalid config format") from e
    return config
