from uuid import UUID

from sqlalchemy import select

from contextos.usuario.tabela import Usuario
from utilitarios.repositorios import RepoLeituraBase


class RepoLeituraUsuario(RepoLeituraBase[Usuario]):
    async def listar(self) -> list[Usuario]:
        return self.sessao.scalars(select(Usuario).order_by(Usuario.nome))

    async def buscar_por_id(self, id: UUID) -> Usuario:
        return await self.sessao.scalar(select(Usuario).filter(Usuario.id == id))

    async def buscar_por_email(self, email: str) -> Usuario:
        return await self.sessao.scalar(select(Usuario).filter(Usuario.email == email))

    async def buscar_por_token(self, token: str) -> Usuario:
        return await self.sessao.scalar(select(Usuario).filter(Usuario.token == token))
