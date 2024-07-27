from uuid import UUID

from fastapi import APIRouter, HTTPException

from contextos.categoria.repositorios.leitura import RepoLeituraCategoria
from contextos.historico.repositorios.escrita import RepoEscritaHistorico
from contextos.historico.repositorios.leitura import RepoLeituraHistorico
from contextos.historico.rotas.modelos import HistoricoEntrada, HistoricoSaida
from contextos.historico.tabela import Historico
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/historicos",
    tags=["Histórico"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("", response_model=HistoricoSaida, status_code=201)
async def criar_historico(historico: HistoricoEntrada, sessao: SessaoUsuario):
    historico = Historico(usuario=sessao.usuario, **historico.model_dump())
    async with RepoEscritaHistorico(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_historico, RepoLeituraCategoria().definir_sessao(
        sessao.sessao
    ) as repo_categoria:
        categoria = await repo_categoria.buscar_por_id(historico.categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Histórico não encontrado")
        historico.categoria = categoria
        await repo_historico.adicionar(historico)
    return HistoricoSaida(**historico.model_dump())


@rotas.get("", response_model=list[HistoricoSaida], status_code=200)
async def listar_historicos(sessao: SessaoUsuario):
    async with RepoLeituraHistorico(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo:
        historicos = await repo.listar()
    return list(map(lambda h: HistoricoSaida(**h.model_dump()), historicos))


@rotas.patch("/{historico_id}", response_model=HistoricoSaida, status_code=200)
async def atualizar_historico(
    historico_id: UUID, historico: HistoricoEntrada, sessao: SessaoUsuario
):
    async with RepoLeituraHistorico(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_leitura:
        instancia_historico = await repo_leitura.buscar_por_id(historico_id)
    if instancia_historico is None:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    if historico.categoria_id != instancia_historico.categoria_id:
        async with RepoLeituraCategoria().definir_sessao(
            sessao.sessao, True
        ) as repo_categoria:
            if historico.categoria_id is None:
                instancia_historico.categoria = None
            else:
                categoria = await repo_categoria.buscar_por_id(historico.categoria_id)
                if categoria is None:
                    raise HTTPException(
                        status_code=404, detail="Histórico não encontrado"
                    )
                instancia_historico.categoria = categoria
    instancia_historico.valor = historico.valor
    instancia_historico.nome = historico.nome
    instancia_historico.data = historico.data
    async with RepoEscritaHistorico(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_escrita:
        await repo_escrita.adicionar(instancia_historico)
    return HistoricoSaida(**instancia_historico.model_dump())


@rotas.delete("/{historico_id}", status_code=204)
async def deletar_historico(historico_id: UUID, sessao: SessaoUsuario):
    async with RepoEscritaHistorico(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo:
        historico = await repo.buscar_por_id(historico_id)
        if historico is None:
            raise HTTPException(status_code=404, detail="Histórico não encontrado")
        await repo.remover(historico)
    return
