from __future__ import annotations

import logging
from typing import Any, Optional

from shortener.adapters.repository import ShortLinkRepository, UserRepository
from shortener.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

logger = logging.getLogger(__name__)

sqlalchemy_database_uri = settings.SQLALCHEMY_DATABASE_URI
async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
default_async_factory = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class UnitOfWork:
    def __init__(
        self,
        session_factory: sessionmaker = default_async_factory,
    ):
        self.session_factory: sessionmaker = session_factory

    def start_repository_session(self, session: Optional[AsyncSession] = None):
        self.session: AsyncSession = session if session else self.session_factory()
        self.users = UserRepository(self.session)
        self.short_links = ShortLinkRepository(self.session)

    async def commit(self):
        await self.session.commit()

    def add(self, obj: Any):
        self.session.add(obj)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        self.start_repository_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
