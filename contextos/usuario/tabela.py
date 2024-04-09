from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.sql.schema import Index, UniqueConstraint

from banco.tabelas import TabelaBase
from utilitarios.senhas import gerar_senha


class Usuario(TabelaBase):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email"),
        Index("idx_nome", "nome"),
        Index("idx_email", "email"),
    )

    nome: Mapped[str]
    email: Mapped[str]
    _senha: Mapped[str]
    token: Mapped[Optional[str]]

    @property
    def senha(self) -> str:
        return self._senha

    @senha.setter
    def senha(self, senha: str) -> None:
        self._senha = gerar_senha(senha)
