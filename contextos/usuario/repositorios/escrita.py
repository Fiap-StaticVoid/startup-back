from sqlalchemy.sql.expression import delete

from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoEscritaBase


class RepoEscritaUsuario(RepoEscritaBase[Usuario]):
    async def adicionar(self, obj: Usuario) -> None:
        self.sessao.add(obj)
        await self.sessao.commit()

    async def remover(self, obj: Usuario) -> None:
        await self.sessao.execute(delete(Usuario).where(Usuario.id == obj.id))
        await self.sessao.commit()

    async def remover_token(self, obj: Usuario) -> None:
        obj.token = None
        await self.sessao.commit()
