from dataclasses import dataclass
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

import banco
from contextos.usuario.repositorios.leitura import RepoLeituraUsuario
from contextos.usuario.tabela import Usuario


@dataclass(frozen=True, slots=True)
class DadosSessao:
    sessao: AsyncSession
    usuario: Usuario


def pegar_token_dos_headers(request: Request) -> str:
    try:
        tipo, token = request.headers.get("Authorization").split(" ")
    except (ValueError, AttributeError) as e:
        raise HTTPException(status_code=401, detail="Token inválido") from e
    if tipo.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token inválido")
    return token


async def pegar_sessao(request: Request) -> AsyncGenerator[DadosSessao, None]:
    token = pegar_token_dos_headers(request)
    async with banco.abrir_sessao() as sessao:
        async with RepoLeituraUsuario().definir_sessao(sessao) as repo:
            usuario = await repo.buscar_por_token(token)
            if usuario is None:
                raise HTTPException(status_code=401, detail="Token inválido")

            yield DadosSessao(sessao=sessao, usuario=usuario)


SessaoUsuario = Annotated[DadosSessao, Depends(pegar_sessao)]
