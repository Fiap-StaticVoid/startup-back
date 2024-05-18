from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from contextos.categoria.rotas import rotas as categoria_rotas
from contextos.historico.rotas import rotas as historico_rotas
from contextos.historico.rotas.lancamento_recorrente import (
    rotas as lancamento_recorrente_rotas,
)
from contextos.usuario.rotas import rotas as usuario_rotas


@asynccontextmanager
async def lifespan(app: FastAPI):
    from banco import iniciar_banco

    await iniciar_banco()
    yield


app = FastAPI(lifespan=lifespan)
origens = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")


api_prefix = "/api"
app.include_router(usuario_rotas, prefix=api_prefix)
app.include_router(categoria_rotas, prefix=api_prefix)
app.include_router(historico_rotas, prefix=api_prefix)
app.include_router(lancamento_recorrente_rotas, prefix=api_prefix)
