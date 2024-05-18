from datetime import datetime, timedelta

from pytest import fixture

from contextos.categoria.tabela import Categoria
from contextos.historico.repositorios.escrita import (
    RepoEscritaHistorico,
    RepoEscritaLancamentoRecorrente,
)
from contextos.historico.tabela import Historico, LancamentoRecorrente, TipoFrequencia
from contextos.usuario.tabela import Usuario


@fixture
async def mock_custom_historico(mock_usuario: Usuario, mock_categoria: Categoria):
    async def wrapper(
        valor: float = 100.0,
        usuario: Usuario = mock_usuario,
        categoria: Categoria = mock_categoria,
        data: datetime = datetime.now(),
    ) -> Historico:
        async with RepoEscritaHistorico(mock_usuario) as repo:
            historico = Historico(
                valor=valor,
                usuario=usuario,
                categoria=categoria,
                data=data,
            )
            await repo.adicionar(historico)

        return historico

    yield wrapper


@fixture
async def mock_custom_lancamento_recorrente(
    mock_usuario: Usuario, mock_categoria: Categoria
):
    agora = datetime.now()

    async def wrapper(
        valor: float = 100.0,
        usuario: Usuario = mock_usuario,
        categoria: Categoria = mock_categoria,
        inicia_em: datetime = agora,
        termina_em: datetime = agora + timedelta(minutes=20),
        frequencia: int = 1,
        tipo_frequencia: TipoFrequencia = TipoFrequencia.minuto,
    ) -> Historico:
        async with RepoEscritaLancamentoRecorrente(mock_usuario) as repo:
            lancamento_recorrente = LancamentoRecorrente(
                valor=valor,
                usuario=usuario,
                categoria=categoria,
                inicia_em=inicia_em,
                termina_em=termina_em,
                frequencia=frequencia,
                tipo_frequencia=tipo_frequencia,
            )
            await repo.adicionar(lancamento_recorrente)

        return lancamento_recorrente

    yield wrapper


@fixture
async def mock_historico(mock_custom_historico):
    yield await mock_custom_historico()


@fixture
async def mock_lancamento_recorrente(mock_custom_lancamento_recorrente):
    yield await mock_custom_lancamento_recorrente()
