from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, Index, UniqueConstraint

from banco.tabelas import TabelaBase
from contextos.usuario.tabela import Usuario


class Categoria(TabelaBase):
    __tablename__ = "categorias"
    __table_args__ = (
        UniqueConstraint(
            "nome",
            "usuario_id",
            name="uq_categoria_nome_usuario_id",
        ),
        Index("idx_categorias_nome", "nome"),
        Index("idx_categorias_usuario_id", "usuario_id"),
    )

    nome: Mapped[str]
    descricao: Mapped[Optional[str]]
    usuario_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    usuario: Mapped[Optional[Usuario]] = relationship("Usuario", lazy="subquery")

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "nome": self.nome,
            "descricao": self.descricao,
            "usuario_id": str(self.usuario_id) if self.usuario_id else None,
        }
