"""pre-criando categorias

Revision ID: 35573f1b667c
Revises: 1fcd87e18a5e
Create Date: 2024-08-26 21:29:20.030335

"""

from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "35573f1b667c"
down_revision: Union[str, None] = "1fcd87e18a5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

categorias = [
    ("Alimentação", "Despesas com alimentação"),
    ("Estudos", "Despesas com estudos"),
    ("Lazer", "Despesas com lazer"),
    ("Salário", "Rendimentos com salário"),
    ("Saúde", "Despesas com saúde"),
    ("Transporte", "Despesas com transporte"),
]


def upgrade() -> None:
    meta = sa.MetaData()
    tabela_categorias = sa.Table("categorias", meta, autoload_with=op.get_bind())

    ids = [str(uuid4()) for _ in categorias]
    op.bulk_insert(
        tabela_categorias,
        [
            {"id": id, "nome": nome, "descricao": descricao}
            for id, (nome, descricao) in zip(ids, categorias)
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM categorias WHERE nome IN :nomes"),
        {"nomes": [nome for nome, _ in categorias]},
    )
