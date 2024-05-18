from uuid import UUID

from fastapi import APIRouter, HTTPException

from contextos.categoria.repositorios.leitura import RepoLeituraCategoria
from contextos.historico.executores.tarefas import criar_historicos_do_lancamento
from contextos.historico.repositorios.escrita import RepoEscritaLancamentoRecorrente
from contextos.historico.repositorios.leitura import RepoLeituraLancamentoRecorrente
from contextos.historico.rotas.modelos import (
    LancamentoRecorrenteEntrada,
    LancamentoRecorrenteSaida,
)
from contextos.historico.tabela import LancamentoRecorrente
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/lancamentos-recorrentes",
    tags=["Lançamento Recorrente"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("", response_model=LancamentoRecorrenteSaida, status_code=201)
async def criar_lancamento_recorrente(
    lancamento_recorrente: LancamentoRecorrenteEntrada, sessao: SessaoUsuario
):
    lancamento_recorrente_instancia = LancamentoRecorrente(
        usuario=sessao.usuario, **lancamento_recorrente.model_dump()
    )
    async with RepoEscritaLancamentoRecorrente(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_lancamento_recorrente, RepoLeituraCategoria().definir_sessao(
        sessao.sessao
    ) as repo_categoria:
        categoria = await repo_categoria.buscar_por_id(
            lancamento_recorrente_instancia.categoria_id
        )
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        lancamento_recorrente_instancia.categoria = categoria
        await repo_lancamento_recorrente.adicionar(lancamento_recorrente_instancia)

    criar_historicos_do_lancamento.delay(lancamento_recorrente_instancia.id)
    return LancamentoRecorrenteSaida(**lancamento_recorrente_instancia.model_dump())


@rotas.get("", response_model=list[LancamentoRecorrenteSaida], status_code=200)
async def listar_lancamentos_recorrentes(sessao: SessaoUsuario):
    async with RepoLeituraLancamentoRecorrente(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo:
        lancamentos_recorrentes = await repo.listar()
    return list(
        map(
            lambda lr: LancamentoRecorrenteSaida(**lr.model_dump()),
            lancamentos_recorrentes,
        )
    )


@rotas.patch(
    "/{lancamento_recorrente_id}",
    response_model=LancamentoRecorrenteSaida,
    status_code=200,
)
async def atualizar_lancamento_recorrente(
    lancamento_recorrente_id: UUID,
    lancamento_recorrente: LancamentoRecorrenteEntrada,
    sessao: SessaoUsuario,
):
    async with RepoLeituraLancamentoRecorrente(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_leitura:
        instancia_lancamento_recorrente = await repo_leitura.buscar_por_id(
            lancamento_recorrente_id
        )
    if instancia_lancamento_recorrente is None:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    if (
        lancamento_recorrente.categoria_id
        != instancia_lancamento_recorrente.categoria_id
    ):
        async with RepoLeituraCategoria().definir_sessao(
            sessao.sessao, True
        ) as repo_categoria:
            categoria = await repo_categoria.buscar_por_id(
                lancamento_recorrente.categoria_id
            )
            if categoria is None:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")
            instancia_lancamento_recorrente.categoria = categoria
    instancia_lancamento_recorrente.valor = lancamento_recorrente.valor
    instancia_lancamento_recorrente.inicia_em = lancamento_recorrente.inicia_em
    instancia_lancamento_recorrente.termina_em = lancamento_recorrente.termina_em
    instancia_lancamento_recorrente.frequencia = lancamento_recorrente.frequencia
    instancia_lancamento_recorrente.tipo_frequencia = (
        lancamento_recorrente.tipo_frequencia
    )
    async with RepoEscritaLancamentoRecorrente(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo_escrita:
        await repo_escrita.adicionar(instancia_lancamento_recorrente)
    criar_historicos_do_lancamento.delay(instancia_lancamento_recorrente.id)
    return LancamentoRecorrenteSaida(**instancia_lancamento_recorrente.model_dump())


@rotas.delete("/{lancamento_recorrente_id}", status_code=204)
async def deletar_lancamento_recorrente(
    lancamento_recorrente_id: UUID, sessao: SessaoUsuario
):
    async with RepoEscritaLancamentoRecorrente(sessao.usuario).definir_sessao(
        sessao.sessao
    ) as repo:
        lancamento_recorrente = await repo.buscar_por_id(lancamento_recorrente_id)
        if lancamento_recorrente is None:
            raise HTTPException(status_code=404, detail="Histórico não encontrado")
        await repo.remover(lancamento_recorrente)
    return
