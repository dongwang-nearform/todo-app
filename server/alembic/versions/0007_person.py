"""person name

Revision ID: 0007_person
Revises: 0006_parent
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0007_person"
down_revision = "0006_parent"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("person_name", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "person_name")
