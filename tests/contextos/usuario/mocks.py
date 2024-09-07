from pytest import fixture

from contextos.usuario.repositorios.escrita import RepoEscritaUsuario
from contextos.usuario.tabela import Usuario


@fixture
async def mock_custom_usuario():
    async def wrapper(
        nome: str = "Usuário Teste",
        email: str = "teste@teste.com.br",
        senha: str = "senha_Forte123",
    ) -> Usuario:
        async with RepoEscritaUsuario() as repo:
            usuario = Usuario(nome=nome, email=email, senha=senha, token="teste")
            await repo.adicionar(usuario)

        return usuario

    yield wrapper


@fixture
async def mock_usuario(mock_custom_usuario):
    yield await mock_custom_usuario()
