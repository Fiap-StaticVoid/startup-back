import asyncio
from contextlib import asynccontextmanager

from httpx import AsyncClient
from pytest import fixture, mark
from pytest_asyncio import fixture as asyncio_fixture
from sqlalchemy.sql import text

pytestmark = mark.asyncio


@asyncio_fixture(scope="session", autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(autouse=True, scope="session")
async def criar_schema():
    import banco
    from banco import tabelas

    async with banco.async_session() as sessao:
        await sessao.execute(text("DROP SCHEMA IF EXISTS testes CASCADE;"))
        await sessao.execute(text("CREATE SCHEMA IF NOT EXISTS testes;"))
        await sessao.commit()
        banco.carregar_tabelas()
        async with banco.async_engine.begin() as conn:
            # muda o esquema para testes
            await conn.execute(text("SET search_path TO testes;"))
            await conn.run_sync(tabelas.Base.metadata.create_all)
    with banco.session() as sessao:
        with banco.engine.begin() as conn:
            # muda o esquema para testes
            conn.execute(text("SET search_path TO testes;"))


@fixture(autouse=True)
async def mock_sessao(monkeypatch):
    class MockAmbiente:
        ASYNC_PG_ENGINE = "asyncpg"
        PG_ENGINE = "psycopg2"
        PG_USER = "postgres"
        PG_PASSWORD = "postgres"
        PG_HOST = "localhost"
        PG_PORT = 5432
        PG_DATABASE = "postgres"
        PG_SCHEMA = "testes"

        @property
        def PG_ASYNC_URL(self):
            return (
                f"postgresql+{self.ASYNC_PG_ENGINE}://{self.PG_USER}:{self.PG_PASSWORD}@"
                f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}?currentSchema={self.PG_SCHEMA}"
            )

        @property
        def PG_URL(self):
            return (
                f"postgresql+{self.PG_ENGINE}://{self.PG_USER}:{self.PG_PASSWORD}@"
                f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}?currentSchema={self.PG_SCHEMA}"
            )

    monkeypatch.setattr("utilitarios.ambiente.ConfigsAmbiente", MockAmbiente)


@fixture(autouse=True)
async def limpar_banco():
    import banco
    from banco import tabelas

    async with banco.async_session() as sessao:
        async with banco.async_engine.begin() as conn:
            await conn.run_sync(tabelas.Base.metadata.drop_all)
            await conn.run_sync(tabelas.Base.metadata.create_all)
        yield sessao
        await sessao.close()


@fixture
async def cliente():
    from servidor.config import app

    @asynccontextmanager
    async def wrapper(token: str | None = None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with AsyncClient(
            app=app, base_url="http://test", headers=headers
        ) as cliente:
            yield cliente

    yield wrapper


from tests.contextos.categoria.mocks import mock_categoria  # noqa: F401, E402
from tests.contextos.categoria.mocks import mock_custom_categoria  # noqa: F401, E402
from tests.contextos.historico.mocks import mock_custom_historico  # noqa: F401, E402
from tests.contextos.historico.mocks import mock_historico  # noqa: F401, E402
from tests.contextos.historico.mocks import (  # noqa: F401, E402
    mock_custom_lancamento_recorrente,
    mock_lancamento_recorrente,
)
from tests.contextos.usuario.mocks import mock_custom_usuario  # noqa: F401, E402
from tests.contextos.usuario.mocks import mock_usuario  # noqa: F401, E402
