from abc import ABC, abstractmethod
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from banco import async_session


class RepoBase:
    sessao: AsyncSession | None

    def __init__(self) -> None:
        self.sessao = None

    async def __aenter__(self) -> Self:
        if self.sessao is None:
            self.sessao = async_session()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.sessao is not None:
            await self.sessao.close()
            self.sessao = None


class RepoEscritaBase[T](RepoBase, ABC):
    @abstractmethod
    async def adicionar(self, obj: T) -> None:
        pass

    @abstractmethod
    async def remover(self, obj: T) -> None:
        pass


class RepoLeituraBase[T](RepoBase, ABC):
    @abstractmethod
    async def listar(self) -> list[T]:
        pass

    @abstractmethod
    async def buscar_por_id(self, id: int) -> T:
        pass
