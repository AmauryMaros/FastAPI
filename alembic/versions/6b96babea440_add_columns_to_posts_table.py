"""add columns to posts table

Revision ID: 6b96babea440
Revises: 64aaa85aaf02
Create Date: 2023-06-12 15:56:47.589465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b96babea440'
down_revision = '64aaa85aaf02'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("published", 
                            sa.Boolean(), 
                            nullable = False, 
                            server_default="TRUE"))
    
    op.add_column("posts", 
                  sa.Column("created_at", 
                            sa.TIMESTAMP(timezone=True),
                            nullable=False, 
                            server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
