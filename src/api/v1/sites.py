from fastapi import APIRouter

from api.v1.dependencies import DbDeps
from sites.schemas import CreateSiteSchema, SetEquipmentSchema
from sites.service import SiteService

router = APIRouter(prefix='/sites')


@router.get('/')
async def get_sites(
    db: DbDeps,
):
    return await SiteService().get_all(db)


@router.post('/')
async def create_site(
    db: DbDeps,
    create_data: CreateSiteSchema
):
    return await SiteService().create(db, create_data)


@router.get('/{site_id}/')
async def get_site(
    db: DbDeps,
    site_id: int
):
    return await SiteService().get(db, site_id)


@router.post('/{site_id}/set_equipment/')
async def set_equipment(
    db: DbDeps,
    site_id: int,
    equipment_schema: SetEquipmentSchema
):
    return await SiteService().set_equipment(
        db,
        site_id,
        equipment_schema.equipment_id
    )