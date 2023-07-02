from abc import ABC, abstractmethod
from typing import Any, Optional

from shortener.adapters.orm import short_links
from shortener.domains.models import ShortLink, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    def get(self, id) -> Any:
        pass


class UserRepository(BaseRepository):
    async def get(self, id) -> Optional[User]:
        statement = select(User).where(User.id == id)
        return await self.session.scalar(statement)

    async def get_by_short_link(self, short_link: ShortLink):
        return (
            self.session.query(User)
            .join(ShortLink)
            .filter(
                short_links.c.source == short_link.source,
            )
            .first()
        )


class ShortLinkRepository(BaseRepository):
    async def get(self, source) -> Optional[ShortLink]:
        statement = select(ShortLink).where(ShortLink.source == source)
        return await self.session.scalar(statement)

    async def get_user(self, user_id) -> Optional[User]:
        statement = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User._short_links))
        )
        return await self.session.scalar(statement)
