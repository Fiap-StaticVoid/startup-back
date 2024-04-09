from datetime import date
from uuid import UUID

from pydantic import BaseModel


class HistoricoEntrada(BaseModel):
    valor: float
    categoria_id: UUID
    data: date


class HistoricoSaida(BaseModel):
    id: UUID
    valor: float
    usuario_id: UUID
    categoria_id: UUID
    data: date
