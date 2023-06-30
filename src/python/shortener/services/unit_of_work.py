from __future__ import annotations

import logging
from typing import Any

from shortener.adapters.repository import ShortLinkRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UOWContext:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.short_links = ShortLinkRepository(session)


class UnitOfWork:
    def __init__(self):
        pass

    def commit(self):
        self.session.commit()

    def add(self, obj: Any):
        self.session.add(obj)

    def __call__(self, session) -> UnitOfWork:
        self.uow_context = UOWContext(session)
        return self

    def __aenter__(self) -> UnitOfWork:
        try:
            self.session
        except Exception as e:
            raise e

        return self

    def __aexit__(self):
        self.uow_context = None

    @property
    def users(self):
        return self.uow_context.users

    @property
    def short_links(self):
        return self.uow_context.short_links

    @property
    def session(self):
        try:
            return self.uow_context.session
        except Exception as e:
            logger.error("Session is not started")
            raise e
