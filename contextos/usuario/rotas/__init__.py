from uuid import UUID

from fastapi import APIRouter

from contextos.usuario.rotas.modelos import (
    DadosLogin,
    TokenSaida,
    UsuarioEntrada,
    UsuarioSaida,
)
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("/login", response_model=TokenSaida, status_code=200)
async def login(dados: DadosLogin):
    pass


@rotas.get("/logout", status_code=200)
async def logout(sessao: SessaoUsuario):
    pass


@rotas.post("/", response_model=UsuarioSaida, status_code=201)
async def criar_usuario(usuario: UsuarioEntrada):
    pass


@rotas.get("/{usuario_id}", response_model=UsuarioSaida, status_code=200)
async def ler_usuario(usuario_id: UUID, sessao: SessaoUsuario):
    pass


@rotas.patch("/{usuario_id}", response_model=UsuarioSaida, status_code=200)
async def atualizar_usuario(
    usuario_id: UUID, usuario: UsuarioEntrada, sessao: SessaoUsuario
):
    pass


@rotas.delete("/{usuario_id}", status_code=204)
async def deletar_usuario(usuario_id: UUID, sessao: SessaoUsuario):
    pass
