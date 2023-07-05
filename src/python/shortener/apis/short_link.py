import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from shortener.adapters.publisher import Publisher
from shortener.domains.events import ShortLinkCreated, ShortLinkUpdated
from shortener.domains.models import ShortLink, User
from shortener.domains.schemas import (
    CreateShortLink,
    ListOfShortLinkResponse,
    ShortLinkResponse,
    UpdateShortLink,
)
from shortener.services.unit_of_work import UnitOfWork

from .dependencies import get_publisher, get_uow

logger = logging.getLogger(__name__)
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


@router.put("/{user_id}/{id}")
async def update_short_link(
    id: str,
    user_id: str,
    cmd: UpdateShortLink,
    uow: UnitOfWork = Depends(get_uow),
    publisher: Publisher = Depends(get_publisher),
):
    try:
        async with uow:
            user: Optional[User] = await uow.short_links.get_user(user_id)
            if not user:
                raise HTTPException(404, "Not found")

            short_link = await uow.short_links.get(id)
            if not user.has_short_link(short_link):
                raise HTTPException(401, "Unauthorized access on short link")

            new_short_link = ShortLink(
                source=cmd.source,
                destination=cmd.destination,
                is_private=cmd.is_private,
            )
            user.delete_short_link(short_link)
            user.register_short_link(new_short_link)

            await uow.commit()
            await publisher.update_cache(
                ShortLinkUpdated(
                    source=cmd.source,
                    destination=cmd.destination,
                    is_private=cmd.is_private,
                )
            )
    except Exception as e:
        await uow.rollback()
        logger.error(str(e))
        raise HTTPException(500, "Cannot commit the operation")
    else:
        return cmd


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
    cmd: CreateShortLink,
    uow: UnitOfWork = Depends(get_uow),
    publisher: Publisher = Depends(get_publisher),
):
    try:
        async with uow:
            uow: UnitOfWork
            user: Optional[User] = await uow.short_links.get_user(cmd.user_id)
            if not user:
                raise HTTPException(404, "Not found")

            short_link = ShortLink(source=cmd.source, destination=cmd.destination)

            if not short_link.is_valid():
                raise HTTPException(400, "Bad request for short link creation")

            if await uow.short_links.get(cmd.source):
                raise HTTPException(
                    422, f"Duplicate short link with source={short_link.source}"
                )

            user.register_short_link(short_link)
            await uow.commit()
            await publisher.create_cache(
                ShortLinkCreated(
                    user_id=cmd.user_id,
                    source=cmd.source,
                    destination=cmd.destination,
                    is_private=cmd.is_private,
                )
            )
    except Exception as e:
        await uow.rollback()
        logger.error(str(e))
        raise HTTPException(500, "Cannot commit the operation")
    else:
        return cmd
