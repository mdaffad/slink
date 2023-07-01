from fastapi import APIRouter, Depends, HTTPException
from shortener.domains.models import User
from shortener.domains.schemas import CreateUser
from shortener.services.unit_of_work import CreateUOW, UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_session

router = APIRouter()


@router.post("/")
async def register_user(
    user_cmd: CreateUser, session: AsyncSession = Depends(get_session)
):
    async with CreateUOW(session) as uow:
        uow: UnitOfWork
        user = User(id=user_cmd.user_id)
        uow.add(user)
        await uow.commit()

    return user_cmd


@router.get("/{id}")
async def get_user(id: str, session: AsyncSession = Depends(get_session)):
    async with CreateUOW(session) as uow:
        uow: UnitOfWork
        user = await uow.users.get(id=id)
        if not user:
            raise HTTPException(404, "Not found")

        return user
