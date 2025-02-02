import enum

from hierarchy.schemas import (
    SiteHierarchySchema,
    FactoryHierarchySchema,
    EquipmentHierarchySchema
)


class ModelType(str, enum.Enum):
    FACTORY = 'factory'
    SITE = 'site'
    EQUIPMENT = 'equipment'

    def __str__(self):
        return self.value


HierarchySchemaType = (
    SiteHierarchySchema | FactoryHierarchySchema | EquipmentHierarchySchema
)
