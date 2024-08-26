from uuid import UUID

from pydantic import BaseModel


class CategoriaEntrada(BaseModel):
    nome: str
    descricao: str | None


class CategoriaSaida(BaseModel):
    id: UUID
    nome: str
    descricao: str | None
