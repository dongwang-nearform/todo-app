"""copies

Revision ID: 0008_copies
Revises: 0007_person
Create Date: 2026-11-04

"""

from alembic import op
import sqlalchemy as sa

revision = "0008_copies"
down_revision = "0007_person"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "copies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_list_id", sa.Integer(), nullable=False),
        sa.Column("destination_list_id", sa.Integer(), nullable=False),
        sa.Column("on_date", sa.Date(), nullable=False),
    )
    op.add_column("todos", sa.Column("copy_id", sa.Integer(), sa.ForeignKey("copies.id"), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "copy_id")
    op.drop_table("copies")
