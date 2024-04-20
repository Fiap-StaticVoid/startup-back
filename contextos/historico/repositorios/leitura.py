from uuid import UUID

from sqlalchemy import select

from contextos.historico.tabela import Historico
from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoLeituraBase


class RepoLeituraHistorico(RepoLeituraBase[Historico]):
    def __init__(self, usuario: Usuario) -> None:
        super().__init__()
        self.usuario = usuario

    async def listar(self) -> list[Historico]:
        return await self.sessao.scalars(
            select(Historico)
            .where(Historico.usuario_id == self.usuario.id)
            .order_by(Historico.data)
        )

    async def buscar_por_id(self, id: UUID) -> Historico | None:
        return await self.sessao.scalar(
            select(Historico).where(
                Historico.id == id,
                Historico.usuario_id == self.usuario.id,
            )
        )
