from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from utilitarios import ambiente

env = ambiente.ConfigsAmbiente()
engine = create_engine(env.PG_URL)
async_engine = create_async_engine(env.PG_ASYNC_URL)


session = sessionmaker(engine, expire_on_commit=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def abrir_sessao():
    async with async_session() as sessao:
        yield sessao


@contextmanager
def abrir_sessao_sync():
    with session() as sessao:
        yield sessao


def carregar_tabelas():
    from contextos.categoria.tabela import Categoria  # noqa: F401
    from contextos.historico.tabela import Historico, LancamentoRecorrente  # noqa: F401
    from contextos.usuario.tabela import Usuario  # noqa: F401


async def iniciar_banco():
    if env.PG_SCHEMA == "teste":
        return
    from banco.tabelas import Base

    carregar_tabelas()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
