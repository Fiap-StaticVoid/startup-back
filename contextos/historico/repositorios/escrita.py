from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.expression import delete

from contextos.historico.tabela import Historico
from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoEscritaBase


class RepoEscritaHistorico(RepoEscritaBase[Historico]):
    def __init__(self, usuario: Usuario) -> None:
        super().__init__()
        self.usuario = usuario

    async def adicionar(self, obj: Historico) -> None:
        self.sessao.add(obj)
        await self.sessao.commit()

    async def remover(self, obj: Historico) -> None:
        await self.sessao.execute(
            delete(Historico).where(
                Historico.id == obj.id, Historico.usuario_id == self.usuario.id
            )
        )
        await self.sessao.commit()

    async def buscar_por_id(self, id: UUID) -> Historico | None:
        return await self.sessao.scalar(
            select(Historico).where(
                Historico.id == id,
                Historico.usuario_id == self.usuario.id,
            )
        )
