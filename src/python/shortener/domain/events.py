from pydantic.dataclasses import dataclass


@dataclass
class ShortLinkCreated:
    pass


@dataclass
class ShortLinkUpdated:
    pass


@dataclass
class ShortLinkDeleted:
    pass


@dataclass
class UserCreated:
    pass


@dataclass
class UserDeleted:
    pass
