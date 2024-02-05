from os import getenv
from pathlib import Path

import yaml


def get_env(name: str) -> str:
    if env := getenv(name):
        return env
    raise RuntimeError(f"Failed to read env variable: {name}")


def read_yaml(file_path: str | Path) -> dict:
    with open(file_path) as file_object:
        data = yaml.load(file_object, Loader=yaml.SafeLoader)
    return data


def get_db_connection_string(db_url: str, driver: str | None = None) -> str:
    driver_formated = "postgresql"
    if driver:
        driver_formated = f"postgresql+{driver}"

    return f"{driver_formated}://{db_url}"
