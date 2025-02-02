from sqlalchemy import select, delete, exists
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import UniversalNameSchema
from db.exceptions import DoesNotExists
from core.schemas import UniversalModelSchema


class BaseModelService:

    model = None

    async def create(
        self,
        session: AsyncSession,
        create_data: UniversalNameSchema
    ) -> UniversalModelSchema:
        query = (
            insert(self.model)
            .values(name=create_data.name)
            .returning(
                self.model.id,
                self.model.name
            )
        )
        cursor = await session.execute(query)
        await session.commit()
        return UniversalModelSchema(**cursor.mappings().first())

    async def delete(
        self,
        session: AsyncSession,
        model_id: int
    ) -> UniversalModelSchema:
        query = (
            delete(self.model)
            .where(self.model.id == model_id)
            .returning(
                self.model.id,
                self.model.name
            )
        )
        cursor = await session.execute(query)
        await session.commit()
        return UniversalModelSchema(**cursor.mappings().first())

    async def get(
        self,
        session: AsyncSession,
        model_id: int
    ) -> UniversalModelSchema:
        query = (
            select(
                self.model.id,
                self.model.name
            )
            .where(self.model.id == model_id)
        )
        cursor = await session.execute(query)
        model_map = cursor.mappings().first()
        if not model_map:
            raise DoesNotExists(f'{model_id=} does not exist!')
        return UniversalModelSchema(**model_map)

    async def exists(
        self,
        session: AsyncSession,
        obj_id: int
    ) -> bool:
        exists_query = exists(self.model).where(
            self.model.id == obj_id
        ).select()
        cursor = await session.execute(exists_query)
        return cursor.scalar()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[UniversalModelSchema]:
        query = (
            select(
                self.model.id,
                self.model.name
            )
        )
        cursor = await session.execute(query)
        return [
            UniversalModelSchema(**data) for data
            in cursor.mappings().all()
        ]
