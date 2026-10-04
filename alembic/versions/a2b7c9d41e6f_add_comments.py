"""add comments

Revision ID: a2b7c9d41e6f
Revises: 8ad23227099c
Create Date: 2026-10-04 12:17:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2b7c9d41e6f"
down_revision: Union[str, Sequence[str], None] = "8ad23227099c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_comments_id", "comments", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_comments_id", table_name="comments")
    op.drop_table("comments")
