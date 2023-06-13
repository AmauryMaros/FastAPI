"""create posts table

Revision ID: e3e0c1cccac8
Revises: 
Create Date: 2023-06-12 15:22:25.380220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3e0c1cccac8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass