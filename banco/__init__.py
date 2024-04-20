from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from utilitarios.ambiente import ConfigsAmbiente

env = ConfigsAmbiente()
engine = create_async_engine(env.PG_URL)


async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def abrir_sessao():
    async with async_session() as sessao:
        yield sessao


def carregar_tabelas():
    from contextos.categoria.tabela import Categoria  # noqa: F401
    from contextos.historico.tabela import Historico  # noqa: F401
    from contextos.usuario.tabela import Usuario  # noqa: F401


async def iniciar_banco():
    from banco.tabelas import Base

    carregar_tabelas()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
