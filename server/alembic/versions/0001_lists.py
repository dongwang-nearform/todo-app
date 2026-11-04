"""lists

Revision ID: 0001_lists
Revises:
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0001_lists"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("lists")
