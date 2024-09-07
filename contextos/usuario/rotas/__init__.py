from uuid import UUID

from fastapi import APIRouter, HTTPException

from contextos.usuario.repositorios.escrita import RepoEscritaUsuario
from contextos.usuario.repositorios.leitura import RepoLeituraUsuario
from contextos.usuario.rotas.erros import SenhaNaoValida
from contextos.usuario.rotas.modelos import (
    DadosLogin,
    TipoToken,
    TokenSaida,
    UsuarioEntrada,
    UsuarioEntradaAtualizar,
    UsuarioSaida,
)
from contextos.usuario.tabela import Usuario
from utilitarios.rotas import SessaoUsuario
from utilitarios.senhas import CheckSenhaForte

rotas = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("/login", response_model=TokenSaida, status_code=200)
async def login(dados: DadosLogin):
    async with RepoLeituraUsuario() as repo:
        usuario = await repo.buscar_por_email(dados.email)
        if usuario is None or not usuario.verificar_senha(dados.senha):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        usuario.gerar_token()
    async with RepoEscritaUsuario() as repo:
        await repo.adicionar(usuario)
    return TokenSaida(token=usuario.token, tipo=TipoToken.bearer)


@rotas.post("/logout", status_code=200)
async def logout(sessao: SessaoUsuario):
    async with RepoEscritaUsuario().definir_sessao(sessao.sessao) as repo:
        usuario = await repo.buscar_por_id(sessao.usuario.id)
        await repo.remover_token(usuario)  # type: ignore
    return


@rotas.post(
    "",
    responses={
        406: {
            "description": "Senha não atende aos requisitos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "falhas": ["falha x", "falha y"],
                        }
                    }
                }
            },
        }
    },
    response_model=UsuarioSaida,
    status_code=201,
)
async def criar_usuario(usuario: UsuarioEntrada):
    senha_eh_forte, falhas = CheckSenhaForte.senha_eh_forte(usuario.senha)
    if not senha_eh_forte:
        raise SenhaNaoValida(falhas)
    usuario = Usuario(**usuario.model_dump())
    async with RepoEscritaUsuario() as repo:
        await repo.adicionar(usuario)
    return UsuarioSaida(**usuario.model_dump())


@rotas.get("/{usuario_id}", response_model=UsuarioSaida, status_code=200)
async def ler_usuario(usuario_id: UUID, sessao: SessaoUsuario):
    async with RepoLeituraUsuario().definir_sessao(sessao.sessao) as repo:
        usuario = await repo.buscar_por_id(usuario_id)
    return UsuarioSaida(**usuario.model_dump())  # type: ignore


@rotas.patch("/{usuario_id}", response_model=UsuarioSaida, status_code=200)
async def atualizar_usuario(
    usuario_id: UUID, usuario: UsuarioEntradaAtualizar, sessao: SessaoUsuario
):
    async with RepoLeituraUsuario().definir_sessao(sessao.sessao, True) as repo_leitura:
        instancia_usuario = await repo_leitura.buscar_por_id(usuario_id)
    if instancia_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    instancia_usuario.nome = usuario.nome
    instancia_usuario.email = usuario.email
    if usuario.senha:
        senha_eh_forte, falhas = CheckSenhaForte.senha_eh_forte(usuario.senha)
        if not senha_eh_forte:
            raise SenhaNaoValida(falhas)
        instancia_usuario.senha = usuario.senha
    async with RepoEscritaUsuario().definir_sessao(sessao.sessao) as repo_escrita:
        await repo_escrita.adicionar(instancia_usuario)
    return UsuarioSaida(**instancia_usuario.model_dump())


@rotas.delete("/deletar", status_code=204)
async def deletar_usuario(sessao: SessaoUsuario):
    async with RepoEscritaUsuario().definir_sessao(sessao.sessao) as repo_escrita:
        await repo_escrita.remover(sessao.usuario)
    return
