from fastapi import APIRouter

from api.v1.dependencies import DbDeps
from core.schemas import UniversalNameSchema
from factory.service import FactoryService

router = APIRouter(prefix='/factory')


@router.get('/')
async def get_factories(
    db: DbDeps,
):
    return await FactoryService().get_all(db)


@router.post('/')
async def create_factory(
    db: DbDeps,
    create_data: UniversalNameSchema
):
    return await FactoryService().create(db, create_data)


@router.get('/{factory_id}/')
async def get_factory(
    db: DbDeps,
    factory_id: int
):
    return await FactoryService().get(db, factory_id)
