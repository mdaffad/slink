from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from shortener.domains.models import ShortLink, User
from shortener.domains.schemas import CreateShortLink
from shortener.services.unit_of_work import CreateUOW, UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_session

router = APIRouter()


@router.get("/{id}")
async def read_short_links(
    id: str, user_id: str, session: AsyncSession = Depends(get_session)
):
    async with CreateUOW(session) as uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.short_links.get_user(user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = await uow.short_links.get(id)
        if not user.has_short_link(short_link):
            return None

        return short_link


@router.post("/")
async def create_short_links(
    short_link_cmd: CreateShortLink, session: AsyncSession = Depends(get_session)
):
    async with CreateUOW(session) as uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.short_links.get_user(short_link_cmd.user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = ShortLink(
            source=short_link_cmd.source, destination=short_link_cmd.destination
        )
        uow.add(short_link)
        if not short_link.is_valid():
            raise HTTPException(400, "Bad request for short link creation")

        if user.has_short_link(short_link):
            raise HTTPException(
                422, f"Duplicate short link with source={short_link.source}"
            )

        user.register_short_link(short_link)
        await uow.commit()
        return short_link_cmd
