import datetime

from httpx import AsyncClient
from pytest import mark

from contextos.categoria.tabela import Categoria
from contextos.historico.executores.tarefas import criar_historicos_do_lancamento
from contextos.historico.repositorios.leitura import RepoLeituraLancamentoRecorrente
from contextos.historico.rotas.modelos import LancamentoRecorrenteEntrada
from contextos.historico.tabela import LancamentoRecorrente, TipoFrequencia
from contextos.usuario.tabela import Usuario

pytestmark = mark.asyncio


async def test_criar_lancamento_recorrente(
    cliente: AsyncClient, mock_usuario: Usuario, mock_categoria: Categoria
):
    agora = datetime.datetime.now()
    uma_hora_depois = agora + datetime.timedelta(hours=1)
    lancamento_recorrente = LancamentoRecorrenteEntrada(
        valor=100.0,
        nome="Lançamento Recorrente Teste",
        categoria_id=mock_categoria.id,
        inicia_em=agora,
        termina_em=uma_hora_depois,
        frequencia=1,
        tipo_frequencia=TipoFrequencia.minuto,
    )
    async with cliente(token=mock_usuario.token) as cliente:
        resposta = await cliente.post(
            "/api/lancamentos-recorrentes",
            json=lancamento_recorrente.model_dump(mode="json"),
        )
    assert resposta.status_code == 201
    async with RepoLeituraLancamentoRecorrente(mock_usuario) as repo:
        assert list(await repo.listar())[0].valor == lancamento_recorrente.valor


async def test_ler_lancamento_recorrente(
    cliente: AsyncClient, mock_lancamento_recorrente: LancamentoRecorrente
):
    async with cliente(token=mock_lancamento_recorrente.usuario.token) as cliente:
        resposta = await cliente.get("/api/lancamentos-recorrentes")
    assert resposta.status_code == 200
    assert resposta.json()[0]["id"] == str(mock_lancamento_recorrente.id)


async def test_atualizar_lancamento_recorrente(
    cliente: AsyncClient, mock_lancamento_recorrente: LancamentoRecorrente
):
    agora = datetime.datetime.now()
    uma_hora_depois = agora + datetime.timedelta(hours=1)
    lancamento_recorrente = LancamentoRecorrenteEntrada(
        valor=200.0,
        nome=mock_lancamento_recorrente.nome,
        categoria_id=mock_lancamento_recorrente.categoria_id,
        inicia_em=agora,
        termina_em=uma_hora_depois,
        frequencia=1,
        tipo_frequencia=TipoFrequencia.minuto,
    )
    async with cliente(token=mock_lancamento_recorrente.usuario.token) as cliente:
        resposta = await cliente.patch(
            f"/api/lancamentos-recorrentes/{mock_lancamento_recorrente.id}",
            json=lancamento_recorrente.model_dump(mode="json"),
        )
    assert resposta.status_code == 200
    async with RepoLeituraLancamentoRecorrente(
        mock_lancamento_recorrente.usuario
    ) as repo:
        assert list(await repo.listar())[0].valor == lancamento_recorrente.valor


async def test_deletar_lancamento_recorrente(
    cliente: AsyncClient, mock_lancamento_recorrente: LancamentoRecorrente
):
    async with cliente(token=mock_lancamento_recorrente.usuario.token) as cliente:
        resposta = await cliente.delete(
            f"/api/lancamentos-recorrentes/{mock_lancamento_recorrente.id}"
        )
    assert resposta.status_code == 204
    async with RepoLeituraLancamentoRecorrente(
        mock_lancamento_recorrente.usuario
    ) as repo:
        assert await repo.buscar_por_id(mock_lancamento_recorrente.id) is None


async def test_rodar_lancamentos_recorrentes(
    monkeypatch, cliente: AsyncClient, mock_lancamento_recorrente: LancamentoRecorrente
):
    agora = datetime.datetime.now() + datetime.timedelta(minutes=5)

    class fakedatetime:
        @classmethod
        def now(cls):
            return agora

    monkeypatch.setattr(datetime, "datetime", fakedatetime)
    criar_historicos_do_lancamento(mock_lancamento_recorrente.id)

    async with cliente(token=mock_lancamento_recorrente.usuario.token) as cliente:
        resposta = await cliente.get("/api/historicos")
    assert resposta.status_code == 200
    assert len(resposta.json()) >= 4
    assert resposta.json()[0]["valor"] == str(mock_lancamento_recorrente.valor)
