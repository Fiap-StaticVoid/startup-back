import datetime
from uuid import UUID

from contextos.historico.repositorios.escrita import RepoEscritaHistorico
from contextos.historico.repositorios.leitura import (
    RepoLeituraHistorico,
    RepoLeituraLancamentoRecorrente,
)
from contextos.historico.tabela import Historico, LancamentoRecorrente
from servidor.celery_config import celery_app


def adicionar_historico_lancamento(
    repo_escrita_historico: RepoEscritaHistorico,
    lancamento: LancamentoRecorrente,
    momento: datetime.datetime,
):
    historico = Historico(
        valor=lancamento.valor,
        nome=lancamento.nome,
        usuario_id=lancamento.usuario_id,
        categoria_id=lancamento.categoria_id,
        data=momento,
        lancamento_id=lancamento.id,
    )
    repo_escrita_historico.adicionar_sync(historico, commit=False)


@celery_app.task
def criar_historicos_do_lancamento(lancamento_id: UUID):
    agora = datetime.datetime.now()

    with RepoLeituraLancamentoRecorrente() as repo_lancamento:
        repo_leitura_historico = RepoLeituraHistorico().definir_sessao_sync(
            repo_lancamento.sessao_sync
        )
        repo_escrita_historico = RepoEscritaHistorico().definir_sessao_sync(
            repo_lancamento.sessao_sync
        )
        lancamento = repo_lancamento.buscar_por_id_sync(lancamento_id)

        if not lancamento:
            return
        if lancamento.inicia_em > agora or (
            lancamento.termina_em and lancamento.termina_em < agora
        ):
            return

        frequencia = lancamento.frequencia_timedelta
        if historicos := list(
            repo_leitura_historico.buscar_historicos_do_lancamento(lancamento_id)
        ):
            ultima_data = historicos[-1].data + frequencia
        else:
            adicionar_historico_lancamento(
                repo_escrita_historico, lancamento, lancamento.inicia_em
            )
            ultima_data = lancamento.inicia_em + frequencia

        while ultima_data < agora:
            adicionar_historico_lancamento(
                repo_escrita_historico, lancamento, ultima_data
            )
            ultima_data += frequencia

        repo_escrita_historico.sessao_sync.commit()


@celery_app.task
def rodar_lancamentos_recorrentes():
    agora = datetime.datetime.now()
    with RepoLeituraLancamentoRecorrente() as repo_lancamento:
        lancamentos = repo_lancamento.listar_crawler(agora)
        for lancamento in lancamentos:
            criar_historicos_do_lancamento.delay(lancamento.id)
