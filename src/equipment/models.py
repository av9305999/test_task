from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.tablenames import EQUIPMENT_TABLE


class Equipment(Base):
    __tablename__ = EQUIPMENT_TABLE

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    site_equipments: Mapped[list['SiteEquipment']] = relationship(
        'SiteEquipment', back_populates='equipment'
    )
