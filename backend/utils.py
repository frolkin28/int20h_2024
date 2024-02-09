from os import getenv
from pathlib import Path

import yaml


def get_env_asserted(key: str) -> str:
    if value := getenv(key):
        return value
    raise RuntimeError(f"Required env variable ({key}) is not set")


def read_yaml(file_path: str | Path) -> dict:
    with open(file_path) as file_object:
        data = yaml.load(file_object, Loader=yaml.SafeLoader)
    return data


def get_from_env_or_file(key: str, file: dict) -> str | None:
    return getenv(key) or file.get(key)
