"""create user table

Revision ID: 03c747f8ac23
Revises: ecee95d88ebd
Create Date: 2023-07-02 11:56:29.457375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03c747f8ac23'
down_revision = 'ecee95d88ebd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer, nullable = False),
                    sa.Column("password", sa.String, nullable = False),
                    sa.Column("email", sa.String, nullable = False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text("now()")),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
