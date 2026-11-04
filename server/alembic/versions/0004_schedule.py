"""date and time

Revision ID: 0004_schedule
Revises: 0003_notes
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0004_schedule"
down_revision = "0003_notes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("on_date", sa.Date(), nullable=True))
    op.add_column("todos", sa.Column("at_time", sa.Time(), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "at_time")
    op.drop_column("todos", "on_date")
