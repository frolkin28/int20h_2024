from os import getenv
from pathlib import Path
from typing import Mapping

import yaml
from flask import jsonify, Response


def success_response(
    status_code: int = 200,
    data: Mapping | None = None,
) -> tuple[Response, int]:
    data = {
        "success": True,
        "data": data,
    }
    return jsonify(data), status_code


def _make_error(error: str | list[str]) -> str:
    if isinstance(error, str):
        return error
    elif isinstance(error, list):
        return ". ".join(error)


def error_response(
    status_code: int,
    errors: Mapping[str, str | list[str]] | None = None,
) -> tuple[Response, int]:
    prepared_errors = {k: _make_error(v) for k, v in errors.items()} if errors else None
    data = {
        "success": False,
        "errors": prepared_errors,
    }

    return jsonify(data), status_code


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
