from pytest import fixture

from contextos.categoria.repositorios.escrita import RepoEscritaCategoria
from contextos.categoria.tabela import Categoria


@fixture
async def mock_custom_categoria():
    async def wrapper(
        nome: str = "Categoria Teste",
        descricao: str | None = "Descrição Teste",
    ) -> Categoria:
        async with RepoEscritaCategoria() as repo:
            categoria = Categoria(nome=nome, descricao=descricao)
            await repo.adicionar(categoria)

        return categoria

    yield wrapper


@fixture
async def mock_categoria(mock_custom_categoria):
    yield await mock_custom_categoria()
