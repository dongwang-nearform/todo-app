"""todos

Revision ID: 0002_todos
Revises: 0001_lists
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0002_todos"
down_revision = "0001_lists"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("list_id", sa.Integer(), sa.ForeignKey("lists.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False, server_default="not_done"),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("copy_confirmed", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.CheckConstraint("state IN ('not_done', 'done')", name="ck_todos_state"),
        sa.CheckConstraint("priority >= 1 AND priority <= 5", name="ck_todos_priority"),
    )


def downgrade() -> None:
    op.drop_table("todos")
