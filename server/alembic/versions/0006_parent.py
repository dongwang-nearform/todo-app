"""sub-to-dos

Revision ID: 0006_parent
Revises: 0005_alarm
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0006_parent"
down_revision = "0005_alarm"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "todos",
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("todos.id", ondelete="CASCADE"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("todos", "parent_id")
