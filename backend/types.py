import typing as t
from datetime import datetime


class SignUpPayload(t.TypedDict):
    first_name: str
    last_name: str
    login: str
    password: str


class SignInPayload(t.TypedDict):
    login: str
    password: str

class AddLotPayload(t.TypedDict):
    lot_name: str
    description: str
    end_date: datetime

