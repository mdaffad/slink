from typing import AsyncGenerator

from shortener.adapters.session import async_session

# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        session: AsyncSession
        yield session
