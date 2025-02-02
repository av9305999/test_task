from fastapi import APIRouter

from api.v1.dependencies import DbDeps
from core.schemas import UniversalNameSchema
from equipment.service import EquipmentService

router = APIRouter(prefix='/equipment')


@router.get('/')
async def get_equipments(
    db: DbDeps,
):
    return await EquipmentService().get_all(db)


@router.post('/')
async def create_equipment(
    db: DbDeps,
    create_data: UniversalNameSchema
):
    return await EquipmentService().create(db, create_data)


@router.get('/{equipment_id}/')
async def get_equipment(
    db: DbDeps,
    equipment_id: int
):
    return await EquipmentService().get(db, equipment_id)
