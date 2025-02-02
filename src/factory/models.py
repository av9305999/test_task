from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.tablenames import FACTORY_TABLE


class Factory(Base):
    __tablename__ = FACTORY_TABLE

    sites: Mapped[list['Site']] = relationship('Site', back_populates='factory')

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
