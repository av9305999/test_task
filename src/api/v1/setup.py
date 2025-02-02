from fastapi import APIRouter

from api.v1.dependencies import DbDeps
from setup_data.create_data import create_data
router = APIRouter(prefix='/setup')


@router.post('/')
async def setup_data(
    db: DbDeps
):
    return await create_data(db)
