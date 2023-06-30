from typing import Generic, Optional, TypeVar

from shortener.adapters.orm import short_links
from shortener.domain.models import ShortLink, User
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, **kwargs) -> Optional[Model]:
        return self.session.query(Model).filter_by(**kwargs).first()

    async def add(self, item: Model):
        await self.session.add(item)


class UserRepository(BaseRepository[User]):
    async def get_by_short_link(self, short_link: ShortLink):
        return (
            self.session.query(User)
            .join(ShortLink)
            .filter(
                short_links.c.source == short_link.source,
            )
            .first()
        )


class ShortLinkRepository(BaseRepository[ShortLink]):
    pass
