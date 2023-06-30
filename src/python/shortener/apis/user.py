from fastapi import APIRouter, Depends, HTTPException
from shortener.domain.models import User
from shortener.domain.schemas import CreateUser
from shortener.services.unit_of_work import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_session

router = APIRouter()


@router.post("/")
async def register_user(
    user_cmd: CreateUser, session: AsyncSession = Depends(get_session)
):
    uow_generator = UnitOfWork()
    async with uow_generator(session) as uow:
        uow: UnitOfWork
        user = User(id=user_cmd.user_id)
        uow.add(user)
        uow.commit()

    return user_cmd


@router.get("/{id}")
async def get_user(id: str, session: AsyncSession = Depends(get_session)):
    uow_generator = UnitOfWork()
    async with uow_generator(session) as uow:
        uow: UnitOfWork
        user = uow.users.get(id=id)
        if not user:
            raise HTTPException(404, "Not found")

        return user
