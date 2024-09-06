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

    def buscar_historicos_do_lancamento(self, lancamento_id: UUID) -> list[Historico]:
        return self.sessao_sync.scalars(
            select(Historico).where(Historico.lancamento_id == lancamento_id)
        )


class RepoLeituraLancamentoRecorrente(RepoLeituraBase[LancamentoRecorrente]):
    def __init__(self, usuario: Usuario | None = None) -> None:
        super().__init__()
        self.usuario = usuario

    def listar_crawler(self, momento: datetime) -> list[LancamentoRecorrente]:
        return self.sessao_sync.scalars(
            select(LancamentoRecorrente)
            .where(
                LancamentoRecorrente.inicia_em <= momento,
                LancamentoRecorrente.termina_em >= momento,
            )
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

    async def buscar_por_id(self, id: UUID) -> LancamentoRecorrente | None:
        if not self.usuario:
            return None
        return await self.sessao.scalar(
            select(LancamentoRecorrente).where(
                LancamentoRecorrente.id == id,
                LancamentoRecorrente.usuario_id == self.usuario.id,
            )
        )

    def buscar_por_id_sync(self, id: UUID) -> LancamentoRecorrente | None:
        return self.sessao_sync.scalar(
            select(LancamentoRecorrente).where(LancamentoRecorrente.id == id)
        )
