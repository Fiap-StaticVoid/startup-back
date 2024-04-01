from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TabelaBase(AbstractConcreteBase, Base):
    id: Mapped[UUID] = mapped_column(UUID_PG, default=uuid4, primary_key=True)
