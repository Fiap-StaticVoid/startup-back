from httpx import AsyncClient
from pytest import mark

from contextos.usuario.repositorios.leitura import RepoLeituraUsuario
from contextos.usuario.rotas.modelos import UsuarioEntrada, UsuarioEntradaAtualizar
from contextos.usuario.tabela import Usuario

pytestmark = mark.asyncio


async def test_criar_usuario(cliente: AsyncClient):
    usuario = UsuarioEntrada(
        nome="Usuário Teste",
        email="teste@teste.com.br",
        senha="senha_Forte123",
    )
    async with cliente() as cliente:
        resposta = await cliente.post("/api/usuarios", json=usuario.model_dump())
    assert resposta.status_code == 201
    async with RepoLeituraUsuario() as repo:
        assert await repo.buscar_por_email(usuario.email) is not None


async def test_ler_usuario(cliente: AsyncClient, mock_usuario: Usuario):
    async with cliente(token="teste") as cliente:
        resposta = await cliente.get(f"/api/usuarios/{mock_usuario.id}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == str(mock_usuario.id)


async def test_atualizar_usuario(cliente: AsyncClient, mock_usuario: Usuario):
    usuario = UsuarioEntradaAtualizar(
        nome="Usuário Teste Atualizado",
        email="teste@teste.com.br",
        senha=None,
    )
    async with cliente(token="teste") as cliente:
        resposta = await cliente.patch(
            f"/api/usuarios/{mock_usuario.id}", json=usuario.model_dump()
        )
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == usuario.nome


async def test_deletar_usuario(cliente: AsyncClient, mock_usuario: Usuario):
    async with cliente(token="teste") as cliente:
        resposta = await cliente.delete("/api/usuarios/deletar")
    assert resposta.status_code == 204
    async with RepoLeituraUsuario() as repo:
        assert await repo.buscar_por_id(mock_usuario.id) is None


async def test_login(cliente: AsyncClient, mock_usuario: Usuario):
    async with cliente(token="teste") as cliente:
        resposta = await cliente.post(
            "/api/usuarios/login",
            json={"email": mock_usuario.email, "senha": "senha"},
        )
    assert resposta.status_code == 200
    assert resposta.json().get("tipo") == "bearer"


async def test_logout(cliente: AsyncClient, mock_usuario: Usuario):
    async with cliente(token="teste") as cliente:
        resposta = await cliente.post(
            "/api/usuarios/logout",
            headers={"Authorization": f"Bearer {mock_usuario.token}"},
        )
    assert resposta.status_code == 200
    async with RepoLeituraUsuario() as repo:
        assert await repo.buscar_por_token(mock_usuario.token) is None
