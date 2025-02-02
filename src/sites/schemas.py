from pydantic import BaseModel

from core.schemas import UniversalNameSchema


class CreateSiteSchema(UniversalNameSchema):
    factory_id: int


class SetEquipmentSchema(BaseModel):
    equipment_id: int


class SiteEquipmentSchema(BaseModel):
    site_id: int
    equipment_id: int
