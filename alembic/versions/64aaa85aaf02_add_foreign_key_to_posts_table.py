"""add foreign key to posts table

Revision ID: 64aaa85aaf02
Revises: 6db7066d02ae
Create Date: 2023-06-12 15:49:30.321265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64aaa85aaf02'
down_revision = '6db7066d02ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("owner_id", sa.Integer(), nullable=False))
    
    op.create_foreign_key("posts_users_fk", 
                          source_table = "posts",
                          referent_table="users", 
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
