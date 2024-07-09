"""Revised user model to support OAuth2

Revision ID: 2602dcc2e19e
Revises: a15bbe989ec1
Create Date: 2024-07-09 20:29:01.000313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2602dcc2e19e'
down_revision: Union[str, None] = 'a15bbe989ec1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('auth_date_hash', sa.String(length=200), nullable=False))
    op.drop_column('users', 'auth_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('auth_date', sa.BIGINT(), autoincrement=False, nullable=False))
    op.drop_column('users', 'auth_date_hash')
    # ### end Alembic commands ###
