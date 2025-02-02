from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session


async def get_db():
    async_session = get_session()
    async with async_session() as session:
        yield session


DbDeps = Annotated[AsyncSession, Depends(get_db)]
