from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from contextos.historico.tabela import TipoFrequencia


class HistoricoEntrada(BaseModel):
    valor: float
    nome: Optional[str]
    categoria_id: Optional[UUID]
    data: datetime


class HistoricoSaida(BaseModel):
    id: UUID
    valor: float
    nome: Optional[str]
    usuario_id: UUID
    categoria_id: Optional[UUID]
    data: datetime
    lancamento_id: Optional[UUID]


class LancamentoRecorrenteEntrada(BaseModel):
    valor: float
    nome: Optional[str]
    categoria_id: Optional[UUID]
    inicia_em: datetime
    termina_em: Optional[datetime]
    frequencia: int
    tipo_frequencia: TipoFrequencia


class LancamentoRecorrenteSaida(BaseModel):
    id: UUID
    valor: float
    nome: Optional[str]
    usuario_id: UUID
    categoria_id: Optional[UUID]
    inicia_em: datetime
    termina_em: Optional[datetime]
    frequencia: int
    tipo_frequencia: TipoFrequencia
