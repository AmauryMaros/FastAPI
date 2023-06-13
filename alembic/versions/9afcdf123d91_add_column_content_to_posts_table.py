"""add column content to posts table

Revision ID: 9afcdf123d91
Revises: e3e0c1cccac8
Create Date: 2023-06-12 15:33:13.068581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9afcdf123d91'
down_revision = 'e3e0c1cccac8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
