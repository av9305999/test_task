from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from equipment.models import Equipment
from factory.models import Factory
from sites.models import Site, SiteEquipment


async def create_factories(
    session: AsyncSession,
    n_factories: int = 3
):
    factory_name = 'Фабрика '
    factory_names = [
        dict(name=f'{factory_name}{i}') for i in range(n_factories)
    ]

    query = (
        insert(Factory)
        .values(factory_names)
        .returning(Factory.id)
    )
    cursor = await session.execute(query)
    return cursor.scalars().all()


async def create_sites(
    session: AsyncSession,
    factory_ids: list[int],
    n_sites: int = 4
):
    site_name = 'Участок '
    site_data = [
        dict(name=f'{site_name}{i}') for i in range(n_sites)
    ]
    site_data[0]['factory_id'] = factory_ids[0]
    site_data[1]['factory_id'] = factory_ids[0]
    site_data[2]['factory_id'] = factory_ids[1]
    site_data[3]['factory_id'] = factory_ids[2]

    query = (
        insert(Site)
        .values(site_data)
        .returning(Site.id)
    )
    cursor = await session.execute(query)
    return cursor.scalars().all()


async def create_equipments(
    session: AsyncSession,
    n_equipments: int = 3
):
    equipment_name = 'Оборудование '
    equipment_names = [
        dict(name=f'{equipment_name}{i}') for i in range(n_equipments)
    ]

    query = (
        insert(Equipment)
        .values(equipment_names)
        .returning(Equipment.id)
    )
    cursor = await session.execute(query)
    return cursor.scalars().all()


async def create_data(session: AsyncSession):

    factories = await create_factories(session)
    sites = await create_sites(session, factories)
    equipments = await create_equipments(session)

    site_equipments = []
    site_equipments.append(
        SiteEquipment(site_id=sites[0], equipment_id=equipments[0])
    )
    site_equipments.append(
        SiteEquipment(site_id=sites[0], equipment_id=equipments[1])
    )
    site_equipments.append(
        SiteEquipment(site_id=sites[1], equipment_id=equipments[0])
    )
    site_equipments.append(
        SiteEquipment(site_id=sites[2], equipment_id=equipments[2])
    )

    session.add_all(site_equipments)
    await session.commit()
