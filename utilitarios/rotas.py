from dataclasses import dataclass
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from banco import abrir_sessao
from contextos.usuario.repositorios.leitura import RepoLeituraUsuario
from contextos.usuario.tabela import Usuario


@dataclass(frozen=True, slots=True)
class DadosSessao:
    sessao: AsyncSession
    usuario: Usuario


def pegar_token_dos_headers(request: Request) -> str:
    try:
        return request.headers.get("Authorization").split(" ")[1]
    except (AttributeError, IndexError) as e:
        raise HTTPException(status_code=401, detail="Token não fornecido") from e


async def pegar_sessao(request: Request) -> AsyncGenerator[DadosSessao, None]:
    token = pegar_token_dos_headers(request)
    async with RepoLeituraUsuario() as repo:
        usuario = await repo.buscar_por_token(token)
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    async with abrir_sessao() as sessao:
        yield DadosSessao(sessao=sessao, usuario=usuario)


SessaoUsuario = Annotated[DadosSessao, Depends(pegar_sessao)]
