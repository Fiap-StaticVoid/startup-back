from dataclasses import dataclass
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from banco import abrir_sessao
from contextos.usuario.repositorios.leitura import RepoLeituraUsuario
from contextos.usuario.tabela import Usuario


@dataclass(slots=True, frozen=True)
class DadosSessao:
    sessao: AsyncSession
    usuario: Usuario


class BearerMiddleware(HTTPBearer):
    async def __call__(self, request: Request) -> AsyncGenerator[DadosSessao, None]:
        credenciais = await super().__call__(request)
        async with abrir_sessao() as sessao:
            async with RepoLeituraUsuario().definir_sessao(sessao) as repo:
                usuario = await repo.buscar_por_token(credenciais.credentials)
                if usuario is None:
                    raise HTTPException(status_code=401, detail="Token inválido")

            yield DadosSessao(sessao=sessao, usuario=usuario)


bearer_middleware = BearerMiddleware()
SessaoUsuario = Annotated[DadosSessao, Depends(bearer_middleware)]
