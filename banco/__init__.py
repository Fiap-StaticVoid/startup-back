from importlib import import_module
from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

BASE_DIR = Path(__file__).parent
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def abrir_sessao():
    async with async_session() as sessao:
        yield sessao


def carregar_tabelas():
    for arquivo in (BASE_DIR / "tabelas").glob("*.py"):
        if arquivo.name != "__init__.py":
            import_module(f"banco.tabelas.{arquivo.stem}")


async def iniciar_banco():
    from banco.tabelas import Base

    carregar_tabelas()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
