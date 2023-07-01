"""SQLAlchemy async engine and sessions tools"""

from shortener.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

sqlalchemy_database_uri = settings.SQLALCHEMY_DATABASE_URI


async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
