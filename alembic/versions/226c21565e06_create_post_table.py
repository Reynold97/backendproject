"""create post table

Revision ID: 226c21565e06
Revises: 
Create Date: 2023-07-02 11:19:01.623461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '226c21565e06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, primary_key = True, nullable = False),
                    sa.Column("title", sa.String, nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
