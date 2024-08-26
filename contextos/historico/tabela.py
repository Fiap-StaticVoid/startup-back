from datetime import datetime, timedelta
from enum import StrEnum
from typing import Optional

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from banco.tabelas import TabelaBase
from contextos.categoria.tabela import Categoria
from contextos.usuario.tabela import Usuario


class TipoFrequencia(StrEnum):
    minuto = "minutos"
    hora = "horas"
    diario = "diario"
    semanal = "semanal"
    mensal = "mensal"
    anual = "anual"


class LancamentoRecorrente(TabelaBase):
    __tablename__ = "lancamentos_recorrentes"

    valor: Mapped[float]
    nome: Mapped[Optional[str]]

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped[Usuario] = relationship("Usuario", lazy="subquery")

    categoria_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categorias.id"), nullable=True
    )
    categoria: Mapped[Optional[Categoria]] = relationship("Categoria", lazy="subquery")

    inicia_em: Mapped[datetime] = mapped_column(default=datetime.today)
    termina_em: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True)
    frequencia: Mapped[int]
    tipo_frequencia: Mapped[TipoFrequencia] = mapped_column(
        ENUM(TipoFrequencia, name="tipo_frequencia")
    )

    @property
    def frequencia_timedelta(self) -> timedelta:
        match self.tipo_frequencia:
            case TipoFrequencia.minuto:
                return timedelta(minutes=self.frequencia)
            case TipoFrequencia.hora:
                return timedelta(hours=self.frequencia)
            case TipoFrequencia.diario:
                return timedelta(days=self.frequencia)
            case TipoFrequencia.semanal:
                return timedelta(weeks=self.frequencia)
            case TipoFrequencia.mensal:
                return timedelta(weeks=self.frequencia * 4)
            case TipoFrequencia.anual:
                return timedelta(weeks=self.frequencia * 52)
        return timedelta()

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "nome": self.nome,
            "valor": self.valor,
            "usuario_id": str(self.usuario_id),
            "categoria_id": str(self.categoria_id) if self.categoria_id else None,
            "inicia_em": self.inicia_em.strftime("%Y-%m-%d"),
            "termina_em": (
                self.termina_em.strftime("%Y-%m-%d") if self.termina_em else None
            ),
            "frequencia": self.frequencia,
            "tipo_frequencia": self.tipo_frequencia.value,
        }


class Historico(TabelaBase):
    __tablename__ = "historicos"

    valor: Mapped[float]

    nome: Mapped[Optional[str]]

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped[Usuario] = relationship("Usuario", lazy="subquery")

    categoria_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categorias.id"), nullable=True
    )
    categoria: Mapped[Optional[Categoria]] = relationship("Categoria", lazy="subquery")

    data: Mapped[datetime] = mapped_column(default=datetime.now)

    lancamento_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lancamentos_recorrentes.id"), nullable=True
    )
    lancamento: Mapped[Optional[LancamentoRecorrente]] = relationship(
        "LancamentoRecorrente", lazy="subquery"
    )

    def model_dump(self) -> dict:
        return {
            "id": str(self.id),
            "nome": self.nome,
            "valor": self.valor,
            "usuario_id": str(self.usuario_id),
            "categoria_id": str(self.categoria_id) if self.categoria_id else None,
            "data": self.data.strftime("%Y-%m-%d"),
            "lancamento_id": str(self.lancamento_id) if self.lancamento_id else None,
        }
