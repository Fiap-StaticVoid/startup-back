from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.expression import delete

from contextos.historico.tabela import Historico, LancamentoRecorrente
from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoEscritaBase


class RepoEscritaHistorico(RepoEscritaBase[Historico]):
    def __init__(self, usuario: Usuario | None = None) -> None:
        super().__init__()
        self.usuario = usuario

    def adicionar_sync(self, obj: Historico, commit: bool = True) -> None:
        self.sessao.add(obj)
        if commit:
            self.sessao_sync.commit()

    async def adicionar(self, obj: Historico, commit: bool = True) -> None:
        self.sessao.add(obj)
        if commit:
            await self.sessao.commit()

    async def remover(self, obj: Historico) -> None:
        if not self.usuario:
            return None
        await self.sessao.execute(
            delete(Historico).where(
                Historico.id == obj.id, Historico.usuario_id == self.usuario.id
            )
        )
        await self.sessao.commit()

    async def buscar_por_id(self, id: UUID) -> Historico | None:
        if not self.usuario:
            return None
        return await self.sessao.scalar(
            select(Historico).where(
                Historico.id == id,
                Historico.usuario_id == self.usuario.id,
            )
        )


class RepoEscritaLancamentoRecorrente(RepoEscritaBase[LancamentoRecorrente]):
    def __init__(self, usuario: Usuario) -> None:
        super().__init__()
        self.usuario = usuario

    async def adicionar(self, obj: LancamentoRecorrente) -> None:
        self.sessao.add(obj)
        await self.sessao.commit()

    async def remover(self, obj: LancamentoRecorrente) -> None:
        await self.sessao.execute(
            delete(LancamentoRecorrente).where(
                LancamentoRecorrente.id == obj.id,
                LancamentoRecorrente.usuario_id == self.usuario.id,
            )
        )
        await self.sessao.commit()

    async def buscar_por_id(self, id: UUID) -> LancamentoRecorrente | None:
        return await self.sessao.scalar(
            select(LancamentoRecorrente).where(
                LancamentoRecorrente.id == id,
                LancamentoRecorrente.usuario_id == self.usuario.id,
            )
        )
