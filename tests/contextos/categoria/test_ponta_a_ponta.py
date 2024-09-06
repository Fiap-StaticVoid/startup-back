from httpx import AsyncClient
from pytest import mark

from contextos.categoria.repositorios.leitura import RepoLeituraCategoria
from contextos.categoria.rotas.modelos import CategoriaEntrada
from contextos.categoria.tabela import Categoria
from contextos.usuario.tabela import Usuario

pytestmark = mark.asyncio


async def test_criar_categoria(cliente: AsyncClient, mock_usuario: Usuario):
    categoria = CategoriaEntrada(
        nome="Categoria Teste",
        descricao="Descrição da categoria teste",
        usuario_id=mock_usuario.id,
    )
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.post(
            "/api/categorias", json=categoria.model_dump(mode="json")
        )
    assert resposta.status_code == 201
    dados = resposta.json()
    async with RepoLeituraCategoria() as repo:
        instancia_categoria = await repo.buscar_por_id(dados["id"])
        assert instancia_categoria is not None
        assert instancia_categoria.nome == categoria.nome
        assert instancia_categoria.descricao == categoria.descricao
        assert instancia_categoria.usuario_id == categoria.usuario_id


async def test_ler_categorias(
    cliente: AsyncClient, mock_usuario: Usuario, mock_categoria: Categoria
):
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.get("/api/categorias")
    assert resposta.status_code == 200
    assert resposta.json()[0]["id"] == str(mock_categoria.id)


async def test_atualizar_categoria(
    cliente: AsyncClient, mock_usuario: Usuario, mock_categoria: Categoria
):
    categoria = CategoriaEntrada(
        nome="Categoria Atualizada",
        descricao="Descrição da categoria atualizada",
        usuario_id=mock_usuario.id,
    )
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.patch(
            f"/api/categorias/{mock_categoria.id}",
            json=categoria.model_dump(mode="json"),
        )
    assert resposta.status_code == 200
    dados = resposta.json()
    async with RepoLeituraCategoria() as repo:
        instancia_categoria = await repo.buscar_por_id(dados["id"])
        assert instancia_categoria is not None
        assert instancia_categoria.nome == categoria.nome
        assert instancia_categoria.descricao == categoria.descricao
        assert instancia_categoria.usuario_id == categoria.usuario_id


async def test_deletar_categoria(
    cliente: AsyncClient, mock_usuario: Usuario, mock_categoria: Categoria
):
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.delete(f"/api/categorias/{mock_categoria.id}")
    assert resposta.status_code == 204
    async with RepoLeituraCategoria() as repo:
        assert (await repo.buscar_por_id(mock_categoria.id)) is None
