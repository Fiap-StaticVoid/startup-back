from datetime import datetime

from contextos.historico.repositorios.escrita import RepoEscritaHistorico
from contextos.historico.repositorios.leitura import (
    RepoLeituraHistorico,
    RepoLeituraLancamentoRecorrente,
)
from contextos.historico.tabela import Historico, LancamentoRecorrente
from servidor.celery import celery_app


def construir_todos_lancamentos_esperados(
    lancamento: LancamentoRecorrente, agora: datetime
) -> list[datetime]:
    lancamentos: list[datetime] = []
    if lancamento.termina_em and lancamento.termina_em < agora:
        return lancamentos
    lancamentos.append(lancamento.inicia_em)
    while True:
        proximo = lancamentos[-1] + lancamento.frequencia_timedelta
        if lancamento.termina_em and proximo > lancamento.termina_em:
            break
        lancamentos.append(proximo)
    return lancamentos


def pegar_lancamento_mais_proximo(
    lancamentos: list[datetime], agora: datetime
) -> datetime:
    for lancamento in lancamentos:
        if lancamento > agora:
            return lancamento
    return lancamentos[-1]


@celery_app.task
def rodar_lancamentos_recorrentes():
    agora = datetime.now()
    with RepoLeituraLancamentoRecorrente() as repo_lancamento:
        repo_leitura_historico = RepoLeituraHistorico().definir_sessao_sync(
            repo_lancamento.sessao_sync
        )
        repo_escrita_historico = RepoEscritaHistorico().definir_sessao_sync(
            repo_lancamento.sessao_sync
        )
        lancamentos = repo_lancamento.listar_crawler(agora)
        for lancamento in lancamentos:
            lancamentos_esperados = construir_todos_lancamentos_esperados(
                lancamento, agora
            )
            if proximo_lancamento := pegar_lancamento_mais_proximo(
                lancamentos_esperados, agora
            ):
                dados = {
                    "valor": lancamento.valor,
                    "usuario_id": lancamento.usuario_id,
                    "categoria_id": lancamento.categoria_id,
                    "data": proximo_lancamento,
                }
                historico = repo_leitura_historico.buscar_exato_crawler(**dados)
                if historico:
                    continue
                repo_escrita_historico.adicionar_sync(
                    Historico(**dados),
                    commit=False,
                )

        repo_escrita_historico.sessao.commit()
