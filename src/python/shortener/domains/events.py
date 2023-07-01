from pydantic import AnyUrl
from pydantic.dataclasses import dataclass


@dataclass
class ShortLinkCreated:
    source: str
    destination: AnyUrl


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
