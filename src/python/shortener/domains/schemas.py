from pydantic import AnyUrl
from pydantic.dataclasses import dataclass


@dataclass
class CreateShortLink:
    user_id: str
    source: str
    destination: AnyUrl


@dataclass
class UpdateShortLink:
    pass


@dataclass
class DeleteShortLink:
    pass


@dataclass
class CreateUser:
    user_id: str


@dataclass
class DeleteUser:
    pass
