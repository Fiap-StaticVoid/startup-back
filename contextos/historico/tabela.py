from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from banco.tabelas import TabelaBase
from contextos.categoria.tabela import Categoria
from contextos.usuario.tabela import Usuario


class Historico(TabelaBase):
    __tablename__ = "historicos"

    valor: Mapped[float]

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped[Usuario] = relationship("Usuario")

    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    categoria: Mapped[Categoria] = relationship("Categoria")

    data: Mapped[date] = mapped_column(default=date.today)
