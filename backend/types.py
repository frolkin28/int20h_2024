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


class LotCreationLoad(t.TypedDict):
    lot_name: str
    description: str
    end_date: datetime
    start_price: float


class LotPayload(t.TypedDict):
    lot_name: str
    description: str
    end_date: datetime


class FullLotPayload(t.TypedDict):
    lot_name: str
    description: str
    start_price: float
    author: dict[str, str, str]
    creation_date: datetime
    end_date: datetime
    pictures: list[str]


class ListLotPayload(t.TypedDict):
    lot_name: str
    lot_id: int
    end_date: datetime
    picture: str
    price: float

class UserForDisplay(t.TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str


class BetForDisplay(t.TypedDict):
    id: int
    lot_id: int
    amount: str
    creation_date: str
    author: UserForDisplay


class MessageForDisplay(t.TypedDict):
    id: int
    content: str
    lot_id: int
    created_at: str
    author: UserForDisplay
