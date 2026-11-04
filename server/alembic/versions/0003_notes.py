"""notes and partial

Revision ID: 0003_notes
Revises: 0002_todos
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0003_notes"
down_revision = "0002_todos"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("notes", sa.String(), nullable=False, server_default=""))
    op.drop_constraint("ck_todos_state", "todos", type_="check")
    op.create_check_constraint(
        "ck_todos_state",
        "todos",
        "state IN ('not_done', 'partial', 'done')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_todos_state", "todos", type_="check")
    op.create_check_constraint("ck_todos_state", "todos", "state IN ('not_done', 'done')")
    op.drop_column("todos", "notes")
