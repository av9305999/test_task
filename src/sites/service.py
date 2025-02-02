from sqlalchemy import exists
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import UniversalModelSchema
from core.service import BaseModelService
from db.exceptions import DoesNotExists, AlreadyExistsError
from equipment.service import EquipmentService
from factory.service import FactoryService
from sites.models import Site, SiteEquipment
from sites.schemas import CreateSiteSchema, SiteEquipmentSchema


class SiteService(BaseModelService):

    model = Site

    def __init__(self):
        self.factory_service = FactoryService()
        self.equipment_service = EquipmentService()

    async def create(
        self,
        session: AsyncSession,
        create_schema: CreateSiteSchema
    ) -> UniversalModelSchema:
        create_data = create_schema.model_dump()
        factory_exists = await self.factory_service.exists(
            session, create_schema.factory_id
        )
        if not factory_exists:
            raise DoesNotExists('No such factory')
        query = (
            insert(self.model)
            .values(create_data)
            .returning(
                self.model.id,
                self.model.name
            )
        )
        cursor = await session.execute(query)
        await session.commit()
        return UniversalModelSchema(**cursor.mappings().first())

    async def exist_site_equipment(
        self,
        session: AsyncSession,
        site_id: int,
        equipment_id: int
    ):
        exists_query = exists(SiteEquipment).where(
            SiteEquipment.site_id == site_id,
            SiteEquipment.equipment_id == equipment_id
        ).select()
        cursor = await session.execute(exists_query)
        return cursor.scalar()

    async def set_equipment(
        self,
        session: AsyncSession,
        site_id: int,
        equipment_id: int
    ) -> SiteEquipmentSchema:
        equipment_exist = await self.equipment_service.exists(
            session, equipment_id
        )
        if not equipment_exist:
            raise DoesNotExists('No such equipment')
        site_exist = await self.exists(
            session, site_id
        )
        if not site_exist:
            raise DoesNotExists('No such site')
        exist_site_equipment = await self.exist_site_equipment(
            session,
            site_id,
            equipment_id
        )
        if exist_site_equipment:
            raise AlreadyExistsError(
                'This equipment already set for this site'
            )
        query = (
            insert(SiteEquipment)
            .values(
                site_id=site_id,
                equipment_id=equipment_id
            )
            .returning(
                SiteEquipment.site_id,
                SiteEquipment.equipment_id
            )
        )
        cursor = await session.execute(query)
        await session.commit()
        return SiteEquipmentSchema(**cursor.mappings().first())
