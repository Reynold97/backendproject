"""complete posts table

Revision ID: 94abf4bb5d61
Revises: 45c1979a661e
Create Date: 2023-07-02 12:21:43.772302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94abf4bb5d61'
down_revision = '45c1979a661e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default = "TRUE", nullable = False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
