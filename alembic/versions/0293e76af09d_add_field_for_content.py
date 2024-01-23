"""add field for content

Revision ID: 0293e76af09d
Revises: 23fae1e1c941
Create Date: 2024-01-23 15:48:33.491395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0293e76af09d'
down_revision: Union[str, None] = '23fae1e1c941'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
