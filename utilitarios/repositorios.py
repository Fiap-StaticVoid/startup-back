from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from banco import async_session

T = TypeVar("T")


class RepoBase:
    sessao: AsyncSession
    manter_sessao_aberta: bool

    def __init__(self) -> None:
        self.sessao = None
        self.manter_sessao_aberta = False

    def definir_sessao(
        self, sessao: AsyncSession, manter_sessao_aberta: bool = False
    ) -> Self:
        self.sessao = sessao
        self.manter_sessao_aberta = manter_sessao_aberta
        return self

    async def __aenter__(self) -> Self:
        if self.sessao is None:
            self.sessao = async_session()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.sessao is not None and not self.manter_sessao_aberta:
            await self.sessao.close()
            self.sessao = None


class RepoEscritaBase(Generic[T], RepoBase, ABC):
    @abstractmethod
    async def adicionar(self, obj: T) -> None:
        pass

    @abstractmethod
    async def remover(self, obj: T) -> None:
        pass


class RepoLeituraBase(Generic[T], RepoBase, ABC):
    @abstractmethod
    async def listar(self) -> list[T]:
        pass

    @abstractmethod
    async def buscar_por_id(self, id: UUID) -> T | None:
        pass
