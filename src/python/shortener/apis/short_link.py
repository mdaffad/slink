from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from shortener.domains.models import ShortLink, User
from shortener.domains.schemas import (
    CreateShortLink,
    ListOfShortLinkResponse,
    ShortLinkResponse,
)
from shortener.services.unit_of_work import UnitOfWork

from .dependencies import get_uow

router = APIRouter()


@router.get("/{user_id}/{id}")
async def get_short_link(id: str, user_id: str, uow: UnitOfWork = Depends(get_uow)):
    async with uow:
        user: Optional[User] = await uow.short_links.get_user(user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = await uow.short_links.get(id)
        if not user.has_short_link(short_link):
            return None

        return short_link


@router.get("/{user_id}")
async def get_short_links(
    user_id: str,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.short_links.get_user(user_id)
        if not user:
            raise HTTPException(404, "Not found")

        return ListOfShortLinkResponse(
            user_id=user.id,
            short_links=[
                ShortLinkResponse(source=item.source, destination=item.destination)
                for item in user._short_links
            ],
        )


@router.post("/")
async def create_short_links(
    short_link_cmd: CreateShortLink,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        uow: UnitOfWork
        user: Optional[User] = await uow.short_links.get_user(short_link_cmd.user_id)
        if not user:
            raise HTTPException(404, "Not found")

        short_link = ShortLink(
            source=short_link_cmd.source, destination=short_link_cmd.destination
        )

        if not short_link.is_valid():
            raise HTTPException(400, "Bad request for short link creation")

        if await uow.short_links.get(short_link_cmd.source):
            raise HTTPException(
                422, f"Duplicate short link with source={short_link.source}"
            )

        user.register_short_link(short_link)
        await uow.commit()
        return short_link_cmd
