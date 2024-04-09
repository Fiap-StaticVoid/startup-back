from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.sql.schema import UniqueConstraint

from banco.tabelas import TabelaBase


class Categoria(TabelaBase):
    __tablename__ = "categorias"
    __table_args__ = (UniqueConstraint("nome"),)

    nome: Mapped[str]
    descricao: Mapped[Optional[str]]
