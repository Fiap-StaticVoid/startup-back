from uuid import UUID

from fastapi import APIRouter

from contextos.categoria.rotas.modelos import CategoriaEntrada, CategoriaSaida
from utilitarios.rotas import SessaoUsuario

rotas = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
    responses={404: {"description": "Não encontrado"}},
)


@rotas.post("/", response_model=CategoriaSaida, status_code=201)
async def criar_categoria(categoria: CategoriaEntrada, sessao: SessaoUsuario):
    pass


@rotas.get("/{categoria_id}", response_model=CategoriaSaida, status_code=200)
async def ler_categoria(categoria_id: UUID, sessao: SessaoUsuario):
    pass


@rotas.get("/", response_model=list[CategoriaSaida], status_code=200)
async def listar_categorias(sessao: SessaoUsuario):
    pass


@rotas.patch("/{categoria_id}", response_model=CategoriaSaida, status_code=200)
async def atualizar_categoria(
    categoria_id: UUID, categoria: CategoriaEntrada, sessao: SessaoUsuario
):
    pass


@rotas.delete("/{categoria_id}", status_code=204)
async def deletar_categoria(categoria_id: UUID, sessao: SessaoUsuario):
    pass
