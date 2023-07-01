from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from shortener.adapters.repository import ShortLinkRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.short_links = ShortLinkRepository(session)

    async def commit(self):
        await self.session.commit()

    def add(self, obj: Any):
        self.session.add(obj)


@asynccontextmanager
async def CreateUOW(session: AsyncSession):
    unit_of_work = UnitOfWork(session)

    yield unit_of_work
