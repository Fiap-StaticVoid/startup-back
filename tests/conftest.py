from asyncio import create_task
from contextlib import asynccontextmanager

from httpx import AsyncClient
from pytest import fixture, mark
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from banco import async_session, carregar_tabelas, engine
from banco.tabelas import Base
from servidor.config import app

pytestmark = mark.asyncio


@fixture(autouse=True)
async def mock_sessao(monkeypatch):
    async with async_session() as sessao:
        await sessao.execute(text("DROP SCHEMA IF EXISTS testes CASCADE;"))
        await sessao.execute(text("CREATE SCHEMA IF NOT EXISTS testes;"))
        await sessao.commit()
        carregar_tabelas()
        async with engine.begin() as conn:
            # muda o esquema para testes
            await conn.execute(text("SET search_path TO testes;"))
            await conn.run_sync(Base.metadata.create_all)

    async def setar_esquema(sessao: AsyncSession):
        await sessao.execute(text("SET search_path TO testes;"))

    @asynccontextmanager
    async def abrir_sessao():
        async with async_session() as sessao:
            await setar_esquema(sessao)
            yield sessao

    def abrir_sessao_permanente():
        sessao = async_session()
        create_task(setar_esquema(sessao))
        return sessao

    monkeypatch.setattr("banco.abrir_sessao", abrir_sessao)
    monkeypatch.setattr("banco.async_session", abrir_sessao_permanente)
    return


@fixture
async def cliente():
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


from tests.contextos.usuario.mocks import mock_custom_usuario  # noqa: F401, E402
from tests.contextos.usuario.mocks import mock_usuario  # noqa: F401, E402
