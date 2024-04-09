from uuid import UUID

from fastapi import APIRouter

from contextos.historico.rotas.modelos import HistoricoEntrada, HistoricoSaida
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/historicos",
    tags=["Histórico"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("/", response_model=HistoricoSaida, status_code=201)
async def criar_historico(historico: HistoricoEntrada, sessao: SessaoUsuario):
    pass


@rotas.get("/{historico_id}", response_model=HistoricoSaida, status_code=200)
async def ler_historico(historico_id: UUID, sessao: SessaoUsuario):
    pass


@rotas.get("/", response_model=list[HistoricoSaida], status_code=200)
async def listar_historicos(sessao: SessaoUsuario):
    pass


@rotas.patch("/{historico_id}", response_model=HistoricoSaida, status_code=200)
async def atualizar_historico(
    historico_id: UUID, historico: HistoricoEntrada, sessao: SessaoUsuario
):
    pass


@rotas.delete("/{historico_id}", status_code=204)
async def deletar_historico(historico_id: UUID, sessao: SessaoUsuario):
    pass
