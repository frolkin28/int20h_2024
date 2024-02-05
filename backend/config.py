from pathlib import Path

from backend.utils import get_env, read_yaml


PROJECT_PATH = Path(__file__).parent.parent


class Config:
    pass


def get_config() -> Config:
    config_path = PROJECT_PATH / get_env("BACKEND_CONFIG_PATH")
    settings_from_file = read_yaml(config_path)
    return settings_from_file
