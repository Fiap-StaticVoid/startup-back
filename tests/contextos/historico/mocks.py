from datetime import date

from pytest import fixture

from contextos.categoria.tabela import Categoria
from contextos.historico.repositorios.escrita import RepoEscritaHistorico
from contextos.historico.tabela import Historico
from contextos.usuario.tabela import Usuario


@fixture
async def mock_custom_historico(mock_usuario: Usuario, mock_categoria: Categoria):
    async def wrapper(
        valor: float = 100.0,
        usuario: Usuario = mock_usuario,
        categoria: Categoria = mock_categoria,
        data: date = date.today(),
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
async def mock_historico(mock_custom_historico):
    yield await mock_custom_historico()
