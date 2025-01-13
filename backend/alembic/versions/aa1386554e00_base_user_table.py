"""base user table

Revision ID: aa1386554e00
Revises: 
Create Date: 2025-01-13 18:49:51.182549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa1386554e00'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'base_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=255), unique=True, nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('base_user')
