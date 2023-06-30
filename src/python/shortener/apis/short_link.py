from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from shortener.domain.models import ShortLink, User
from shortener.domain.schemas import CreateShortLink
from shortener.services.unit_of_work import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_session

router = APIRouter()


@router.get("/{id}")
async def read_short_links(
    id: str, user_id: str, session: AsyncSession = Depends(get_session)
):
    uow_generator = UnitOfWork()
    async with uow_generator(session) as uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.users.get(id=user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = await uow.short_links.get(id=id)
        if not user.has_short_link(short_link):
            return None

        return short_link


@router.post("/")
async def create_short_links(
    short_link_cmd: CreateShortLink, session: AsyncSession = Depends(get_session)
):
    uow_generator = UnitOfWork()
    async with uow_generator(session) as uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.users.get(id=short_link_cmd.user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = ShortLink(
            source=short_link_cmd.source, destination=short_link_cmd.destination
        )
        if not short_link.is_valid():
            pass

        user.register_short_link(short_link)
        uow.commit()
