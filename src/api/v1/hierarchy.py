from fastapi import APIRouter

from api.v1.dependencies import DbDeps
from hierarchy.types import ModelType
from hierarchy.service import get_hierarchy

router = APIRouter(prefix='/hierarchy')


@router.get('/')
async def get_model_hierarchy(
    db: DbDeps,
    model_type: ModelType = ModelType.EQUIPMENT
):
    return await get_hierarchy(db, model_type)
