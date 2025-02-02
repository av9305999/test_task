from pydantic import BaseModel, Field


class EquipmentHierarchySchema(BaseModel):
    equipment: str
    equipment_id: int
    sites: list[str | None] = Field(default_factory=list)
    factories: list[str | None] = Field(default_factory=list)


class FactoryHierarchySchema(BaseModel):
    factory: str
    factory_id: int
    sites: list[str] = Field(default_factory=list)
    equipments: list[str | None] = Field(default_factory=list)


class SiteHierarchySchema(BaseModel):
    site: str
    site_id: int
    equipments: list[str | None] = Field(default_factory=list)
    factory: str
