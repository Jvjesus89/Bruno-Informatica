"""create_solicitacao_compra_table

Revision ID: 3d9007205250
Revises: f5b312378bfa
Create Date: 2026-06-13 21:16:13.554721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d9007205250'
down_revision: Union[str, None] = 'f5b312378bfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands manually adjusted - create solicitacao_compra table ###
    op.create_table('solicitacoes_compra',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('idos', sa.Uuid(), nullable=False),
    sa.Column('idproduto', sa.Uuid(), nullable=False),
    sa.Column('idtecnico', sa.Uuid(), nullable=False),
    sa.Column('quantidade_solicitada', sa.Integer(), nullable=False),
    sa.Column('status_solicitacao', sa.String(length=30), nullable=False), # Pendente, Aprovado, Rejeitado
    sa.Column('data_solicitacao', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idos'], ['OS.idos'], ondelete='RESTRICT'), # Garante o cenário de borda que discutimos (impedir exclusão)
    sa.ForeignKeyConstraint(['idproduto'], ['produtos.idproduto'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['idtecnico'], ['usuario.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands manually adjusted ###
    op.drop_table('solicitacoes_compra')
    # ### end Alembic commands ###