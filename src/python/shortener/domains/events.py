from pydantic import AnyUrl
from pydantic.dataclasses import dataclass


@dataclass
class ShortLinkCreated:
    user_id: str
    source: str
    destination: AnyUrl
    is_private: bool


@dataclass
class ShortLinkUpdated:
    source: str
    destination: AnyUrl


@dataclass
class ShortLinkDeleted:
    pass


@dataclass
class UserCreated:
    pass


@dataclass
class UserDeleted:
    pass
