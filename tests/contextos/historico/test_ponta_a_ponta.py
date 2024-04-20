from datetime import date

from httpx import AsyncClient
from pytest import mark

from contextos.categoria.tabela import Categoria
from contextos.historico.repositorios.leitura import RepoLeituraHistorico
from contextos.historico.rotas.modelos import HistoricoEntrada
from contextos.historico.tabela import Historico
from contextos.usuario.tabela import Usuario

pytestmark = mark.asyncio


async def test_criar_historico(
    cliente: AsyncClient, mock_usuario: Usuario, mock_categoria: Categoria
):
    historico = HistoricoEntrada(
        valor=100.0,
        categoria_id=mock_categoria.id,
        data=date.today(),
    )
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.post(
            "/api/historicos", json=historico.model_dump(mode="json")
        )
    assert resposta.status_code == 201
    async with RepoLeituraHistorico(mock_usuario) as repo:
        assert list(await repo.listar())[0].valor == historico.valor


async def test_ler_historicos(cliente: AsyncClient, mock_historico: Historico):
    async with cliente(token=mock_historico.usuario.token) as cliente:
        resposta = await cliente.get("/api/historicos")
    assert resposta.status_code == 200
    assert resposta.json()[0]["id"] == str(mock_historico.id)


async def test_atualizar_historico(cliente: AsyncClient, mock_historico: Historico):
    historico = HistoricoEntrada(
        valor=200.0,
        categoria_id=mock_historico.categoria_id,
        data=date.today(),
    )
    async with cliente(token=mock_historico.usuario.token) as cliente:
        resposta = await cliente.patch(
            f"/api/historicos/{mock_historico.id}",
            json=historico.model_dump(mode="json"),
        )
    assert resposta.status_code == 200
    async with RepoLeituraHistorico(mock_historico.usuario) as repo:
        assert list(await repo.listar())[0].valor == historico.valor


async def test_deletar_historico(cliente: AsyncClient, mock_historico: Historico):
    async with cliente(token=mock_historico.usuario.token) as cliente:
        resposta = await cliente.delete(f"/api/historicos/{mock_historico.id}")
    assert resposta.status_code == 204
    async with RepoLeituraHistorico(mock_historico.usuario) as repo:
        assert await repo.buscar_por_id(mock_historico.id) is None
