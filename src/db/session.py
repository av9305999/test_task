from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

from config import settings


def get_session():
    engine = create_async_engine(settings.get_postgres_dsn())
    return async_sessionmaker(engine, expire_on_commit=False)
