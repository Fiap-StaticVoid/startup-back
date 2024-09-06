from uuid import UUID

from sqlalchemy import or_, select

from contextos.categoria.tabela import Categoria
from utilitarios.repositorios import RepoLeituraBase


class RepoLeituraCategoria(RepoLeituraBase[Categoria]):
    async def buscar_do_usuario(self, usuario_id: UUID) -> list[Categoria]:
        return await self.sessao.scalars(
            select(Categoria)
            .where(
                or_(
                    Categoria.usuario_id == usuario_id,
                    Categoria.usuario_id.is_(None),
                )
            )
            .order_by(Categoria.nome)
        )

    async def listar(self) -> list[Categoria]:
        return await self.sessao.scalars(select(Categoria).order_by(Categoria.nome))

    async def buscar_por_id(self, id: UUID) -> Categoria | None:
        return await self.sessao.scalar(
            select(Categoria).where(
                Categoria.id == id,
            )
        )
