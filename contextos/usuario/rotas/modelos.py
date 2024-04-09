from uuid import UUID

from pydantic import BaseModel


class DadosLogin(BaseModel):
    email: str
    senha: str


class UsuarioEntrada(DadosLogin):
    nome: str


class UsuarioSaida(BaseModel):
    id: UUID
    nome: str
    email: str


class TokenSaida(BaseModel):
    token: str
