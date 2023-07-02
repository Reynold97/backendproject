"""add foreign key to post table

Revision ID: 45c1979a661e
Revises: 03c747f8ac23
Create Date: 2023-07-02 12:08:40.490332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45c1979a661e'
down_revision = '03c747f8ac23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable = False))
    op.create_foreign_key("posts_users_fk", source_table= "posts", referent_table= "users", local_cols=["owner_id"],
                          remote_cols=["id"], ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name= "posts")
    op.drop_column("posts", "owner_id")
    pass
