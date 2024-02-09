import typing as t

from datetime import datetime


class SignUpPayload(t.TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str


class SignInPayload(t.TypedDict):
    email: str
    password: str


class AddLotPayload(t.TypedDict):
    lot_name: str
    description: str
    end_date: datetime


class UserForDisplay(t.TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str


class BetForDisplay(t.TypedDict):
    id: int
    lot_id: int
    amount: int
    creation_date: str
    author: UserForDisplay
