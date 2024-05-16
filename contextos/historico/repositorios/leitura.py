from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from contextos.historico.tabela import Historico, LancamentoRecorrente
from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoLeituraBase


class RepoLeituraHistorico(RepoLeituraBase[Historico]):
    def __init__(self, usuario: Usuario | None = None) -> None:
        super().__init__()
        self.usuario = usuario

    async def listar(self) -> list[Historico]:
        if not self.usuario:
            return []
        return await self.sessao.scalars(
            select(Historico)
            .where(Historico.usuario_id == self.usuario.id)
            .order_by(Historico.data)
        )

    async def buscar_por_id(self, id: UUID) -> Historico | None:
        if not self.usuario:
            return None
        return await self.sessao.scalar(
            select(Historico).where(
                Historico.id == id,
                Historico.usuario_id == self.usuario.id,
            )
        )

    def buscar_exato_crawler(
        self,
        valor: float,
        usuario_id: int,
        categoria_id: int,
        data: datetime,
    ) -> list[Historico]:
        return self.sessao_sync.scalars(
            select(Historico)
            .where(Historico.valor == valor)
            .where(Historico.usuario_id == usuario_id)
            .where(Historico.categoria_id == categoria_id)
            .where(Historico.data == data)
            .order_by(Historico.data)
        )


class RepoLeituraLancamentoRecorrente(RepoLeituraBase[LancamentoRecorrente]):
    def __init__(self, usuario: Usuario | None = None) -> None:
        super().__init__()
        self.usuario = usuario

    def listar_crawler(self, momento: datetime) -> list[LancamentoRecorrente]:
        return self.sessao_sync.scalars(
            select(LancamentoRecorrente)
            .where(LancamentoRecorrente.inicia_em <= momento)
            .where(LancamentoRecorrente.termina_em >= momento)
            .order_by(LancamentoRecorrente.inicia_em)
        )

    async def listar(self) -> list[LancamentoRecorrente]:
        if not self.usuario:
            return []
        return await self.sessao.scalars(
            select(LancamentoRecorrente)
            .where(LancamentoRecorrente.usuario_id == self.usuario.id)
            .order_by(LancamentoRecorrente.inicia_em)
        )

    async def buscar_por_id(self, id: UUID) -> Historico | None:
        if not self.usuario:
            return None
        return await self.sessao.scalar(
            select(LancamentoRecorrente).where(
                LancamentoRecorrente.id == id,
                LancamentoRecorrente.usuario_id == self.usuario.id,
            )
        )
