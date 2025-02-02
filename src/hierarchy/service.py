from abc import ABC, abstractmethod

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from equipment.models import Equipment
from factory.models import Factory
from sites.models import Site, SiteEquipment
from hierarchy.schemas import (
    SiteHierarchySchema,
    FactoryHierarchySchema,
    EquipmentHierarchySchema
)
from hierarchy.types import ModelType, HierarchySchemaType


class HierarchyInterface(ABC):

    hierarchy_schema: HierarchySchemaType = None

    @abstractmethod
    def get_query(self) -> Select:
        raise NotImplementedError

    async def get_hierarchy(
        self,
        session: AsyncSession
    ) -> list[HierarchySchemaType]:
        query = self.get_query()
        cursor = await session.execute(query)
        return [
            self.hierarchy_schema(**data) for data in cursor.mappings().all()
        ]


class EquipmentHierarchy(HierarchyInterface):
    hierarchy_schema = EquipmentHierarchySchema

    def get_query(self) -> Select:
        return (
            select(
                Equipment.id.label('equipment_id'),
                Equipment.name.label('equipment'),
                func.array_agg(Site.name).label('sites'),
                func.array_agg(Factory.name).label('factories'),
            )
            .outerjoin(
                SiteEquipment, SiteEquipment.equipment_id == Equipment.id
            )
            .join(
                Site, SiteEquipment.site_id == Site.id
            )
            .join(Factory, Factory.id == Site.factory_id)
            .group_by(Equipment.id, Equipment.name)
        )


class SiteHierarchy(HierarchyInterface):
    hierarchy_schema = SiteHierarchySchema

    def get_query(self) -> Select:
        return (
            select(
                Site.id.label('site_id'),
                Site.name.label('site'),
                Factory.name.label('factory'),
                func.array_agg(Equipment.name).label('equipments')
            )
            .join(Factory, Factory.id == Site.factory_id)
            .outerjoin(
                SiteEquipment, SiteEquipment.site_id == Site.id
            )
            .outerjoin(Equipment, Equipment.id == SiteEquipment.equipment_id)
            .group_by(Site.id, Site.name, Factory.name)
        )


class FactoryHierarchy(HierarchyInterface):
    hierarchy_schema = FactoryHierarchySchema

    def get_query(self) -> Select:
        return (
            select(
                Factory.id.label('factory_id'),
                Factory.name.label('factory'),
                func.array_agg(Site.name).label('sites'),
                func.array_agg(Equipment.name).label('equipments')
            )
            .join(
                Site, Site.factory_id == Factory.id
            )
            .outerjoin(
                SiteEquipment, SiteEquipment.site_id == Site.id
            )
            .outerjoin(
                Equipment, Equipment.id == SiteEquipment.equipment_id
            )
            .group_by(Factory.id, Factory.name)
        )


async def get_hierarchy(
    session: AsyncSession,
    model_type: ModelType = ModelType.EQUIPMENT
) -> list[HierarchySchemaType]:
    hierarchy_map = {
        ModelType.FACTORY: FactoryHierarchy,
        ModelType.SITE: SiteHierarchy,
        ModelType.EQUIPMENT: EquipmentHierarchy
    }
    hierarchy_cls = hierarchy_map[model_type]
    return await hierarchy_cls().get_hierarchy(session)
