import typing as t


class SignUpPayload(t.TypedDict):
    first_name: str
    last_name: str
    login: str
    password: str


class SignInPayload(t.TypedDict):
    login: str
    password: str
