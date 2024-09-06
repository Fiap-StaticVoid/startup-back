from secrets import token_urlsafe
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.sql.schema import Index, UniqueConstraint

from banco.tabelas import TabelaBase
from utilitarios.senhas import gerar_senha, verificar_senha


class Usuario(TabelaBase):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email"),
        Index("idx_usuarios_nome", "nome"),
        Index("idx_usuarios_email", "email"),
        Index("idx_usuarios_token", "token"),
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

    def gerar_token(self) -> None:
        self.token = token_urlsafe(64)

    def verificar_senha(self, senha: str) -> bool:
        return verificar_senha(senha, self._senha)

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "nome": self.nome,
            "email": self.email,
            "token": self.token,
        }
