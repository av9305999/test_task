from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from db.base import Base
from db.tablenames import (
    SITE_TABLE,
    FACTORY_TABLE,
    SITE_EQUIPMENT_TABLE,
    EQUIPMENT_TABLE
)


class Site(Base):
    __tablename__ = SITE_TABLE

    factory_id: Mapped[int] = mapped_column(
        ForeignKey(f'{FACTORY_TABLE}.id', ondelete="CASCADE")
    )
    factory: Mapped['Factory'] = relationship(back_populates='sites')

    site_equipments: Mapped[list['SiteEquipment']] = relationship(
        back_populates='site'
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class SiteEquipment(Base):
    __tablename__ = SITE_EQUIPMENT_TABLE
    __table_args__ = (
        UniqueConstraint(
            'site_id', 'equipment_id'
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    site_id: Mapped[int] = mapped_column(
        ForeignKey(f'{SITE_TABLE}.id', ondelete="CASCADE")
    )
    site: Mapped['Site'] = relationship(
        back_populates='site_equipments', remote_side='Site.id'
    )

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey(f'{EQUIPMENT_TABLE}.id', ondelete="CASCADE")
    )
    equipment: Mapped['Equipment'] = relationship(
        back_populates='site_equipments',
        remote_side='Equipment.id'
    )
