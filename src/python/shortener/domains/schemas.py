from typing import List

from pydantic import AnyUrl, Field
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


@dataclass
class ShortLinkResponse:
    source: str
    destination: AnyUrl


@dataclass
class ListOfShortLinkResponse:
    user_id: str
    short_links: List[ShortLinkResponse] = Field(default_factory=list)
