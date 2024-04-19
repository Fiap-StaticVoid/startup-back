from contextlib import asynccontextmanager
from importlib import import_module
from pathlib import Path

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
    for arquivo in (Path(__file__).parent / "tabelas").glob("*.py"):
        if arquivo.name != "__init__.py":
            import_module(f"banco.tabelas.{arquivo.stem}")


async def iniciar_banco():
    from banco.tabelas import Base

    carregar_tabelas()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
