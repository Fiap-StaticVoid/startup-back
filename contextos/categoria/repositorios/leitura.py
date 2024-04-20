from uuid import UUID

from sqlalchemy import select

from contextos.categoria.tabela import Categoria
from utilitarios.repositorios import RepoLeituraBase


class RepoLeituraCategoria(RepoLeituraBase[Categoria]):
    async def listar(self) -> list[Categoria]:
        return await self.sessao.scalars(select(Categoria).order_by(Categoria.nome))

    async def buscar_por_id(self, id: UUID) -> Categoria | None:
        return await self.sessao.scalar(
            select(Categoria).where(
                Categoria.id == id,
            )
        )
