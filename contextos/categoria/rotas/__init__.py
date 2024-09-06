from uuid import UUID

from fastapi import APIRouter, HTTPException

from contextos.categoria.repositorios.escrita import RepoEscritaCategoria
from contextos.categoria.repositorios.leitura import RepoLeituraCategoria
from contextos.categoria.rotas.modelos import CategoriaEntrada, CategoriaSaida
from contextos.categoria.tabela import Categoria
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("", response_model=CategoriaSaida, status_code=201)
async def criar_categoria(categoria: CategoriaEntrada, sessao: SessaoUsuario):
    categoria = Categoria(**categoria.model_dump(), usuario_id=sessao.usuario.id)
    async with RepoEscritaCategoria().definir_sessao(sessao.sessao) as repo:
        await repo.adicionar(categoria)
    return CategoriaSaida(**categoria.model_dump())


@rotas.get("", response_model=list[CategoriaSaida], status_code=200)
async def listar_categorias(sessao: SessaoUsuario):
    async with RepoLeituraCategoria().definir_sessao(sessao.sessao) as repo:
        categorias = await repo.buscar_do_usuario(sessao.usuario.id)
    return list(map(lambda h: CategoriaSaida(**h.model_dump()), categorias))


@rotas.patch("/{categoria_id}", response_model=CategoriaSaida, status_code=200)
async def atualizar_categoria(
    categoria_id: UUID, categoria: CategoriaEntrada, sessao: SessaoUsuario
):
    async with RepoLeituraCategoria().definir_sessao(
        sessao.sessao, True
    ) as repo_leitura:
        instancia_categoria = await repo_leitura.buscar_por_id(categoria_id)
    if instancia_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    instancia_categoria.nome = categoria.nome
    instancia_categoria.descricao = categoria.descricao
    async with RepoEscritaCategoria().definir_sessao(sessao.sessao) as repo_escrita:
        await repo_escrita.adicionar(instancia_categoria)
    return CategoriaSaida(**instancia_categoria.model_dump())


@rotas.delete("/{categoria_id}", status_code=204)
async def deletar_categoria(categoria_id: UUID, sessao: SessaoUsuario):
    async with RepoEscritaCategoria().definir_sessao(sessao.sessao) as repo:
        categoria = await repo.buscar_por_id(categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrado")
        await repo.remover(categoria)
    return None
