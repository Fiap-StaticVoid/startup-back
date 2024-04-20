from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.expression import delete

from contextos.categoria.tabela import Categoria
from utilitarios.repositorios import RepoEscritaBase


class RepoEscritaCategoria(RepoEscritaBase[Categoria]):
    async def adicionar(self, obj: Categoria) -> None:
        self.sessao.add(obj)
        await self.sessao.commit()

    async def remover(self, obj: Categoria) -> None:
        await self.sessao.execute(delete(Categoria).where(Categoria.id == obj.id))
        await self.sessao.commit()

    async def buscar_por_id(self, id: UUID) -> Categoria | None:
        return await self.sessao.scalar(
            select(Categoria).where(
                Categoria.id == id,
            )
        )
