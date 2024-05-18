from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from contextos.historico.tabela import TipoFrequencia


class HistoricoEntrada(BaseModel):
    valor: float
    categoria_id: UUID
    data: datetime


class HistoricoSaida(BaseModel):
    id: UUID
    valor: float
    usuario_id: UUID
    categoria_id: UUID
    data: datetime


class LancamentoRecorrenteEntrada(BaseModel):
    valor: float
    categoria_id: UUID
    inicia_em: datetime
    termina_em: Optional[datetime]
    frequencia: int
    tipo_frequencia: TipoFrequencia


class LancamentoRecorrenteSaida(BaseModel):
    id: UUID
    valor: float
    usuario_id: UUID
    categoria_id: UUID
    inicia_em: datetime
    termina_em: Optional[datetime]
    frequencia: int
    tipo_frequencia: TipoFrequencia
