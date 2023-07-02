from fastapi import APIRouter, Depends, HTTPException
from shortener.domains.models import User
from shortener.domains.schemas import CreateUser
from shortener.services.unit_of_work import UnitOfWork

from .dependencies import get_uow

router = APIRouter()


@router.post("/")
async def register_user(
    user_cmd: CreateUser,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        uow: UnitOfWork
        user = User(id=user_cmd.user_id)
        uow.add(user)
        await uow.commit()

    return user_cmd


@router.get("/{id}")
async def get_user(
    id: str,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        uow: UnitOfWork
        user = await uow.users.get(id=id)
        print("test")
        if not user:
            raise HTTPException(404, "Not found")

        return user
