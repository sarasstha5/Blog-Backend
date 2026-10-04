"""add post likes

Revision ID: b4e6a91c2f73
Revises: a2b7c9d41e6f
Create Date: 2026-10-04 13:22:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4e6a91c2f73"
down_revision: Union[str, Sequence[str], None] = "a2b7c9d41e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_likes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )


def downgrade() -> None:
    op.drop_table("post_likes")
