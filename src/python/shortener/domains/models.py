from typing import Set, Union
from uuid import UUID


class ShortLink:
    def __init__(self, source: str, destination: str, is_private: bool = False) -> None:
        self.source = source
        self.destination = destination
        self.is_private = is_private

    def is_empty(self):
        if self.source == "":
            return True
        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, ShortLink):
            return False
        return other.source == self.source

    def __hash__(self):
        return hash(self.source)

    def is_valid(self) -> bool:
        if self.is_empty():
            return False
        return True


class User:
    def __init__(self, id: Union[str, UUID]) -> None:
        self.id: str = id if isinstance(id, str) else str(id)
        self._short_links: Set[ShortLink] = set()

    def register_short_link(self, short_link: ShortLink) -> None:
        self._short_links.add(short_link)

    def delete_short_link(self, short_link: ShortLink) -> None:
        self._short_links.discard(short_link)

    def is_short_link_valid(self, new_short_link: ShortLink) -> bool:
        if not new_short_link.is_valid():
            return False
        return True

    def has_short_link(self, short_link: ShortLink) -> bool:
        if short_link in self._short_links:
            return True
        return False

    def can_update_short_link(self, new_short_link: ShortLink) -> bool:
        return self.has_short_link(new_short_link) and self.is_short_link_valid(
            new_short_link
        )

    def update_short_links(self, new_short_link: ShortLink) -> None:
        if self.can_update_short_link(new_short_link):
            self._short_links.update([new_short_link])

    def __repr__(self):
        return f"<User {self.id}>"
