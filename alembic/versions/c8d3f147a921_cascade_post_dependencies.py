"""cascade deletes for post dependencies

Revision ID: c8d3f147a921
Revises: 3bb1fe6ce5f9
Create Date: 2026-10-08 15:32:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c8d3f147a921"
down_revision: Union[str, Sequence[str], None] = "3bb1fe6ce5f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("post_likes_post_id_fkey", "post_likes", type_="foreignkey")
    op.create_foreign_key(
        "post_likes_post_id_fkey",
        "post_likes",
        "posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("bookmarks_post_id_fkey", "bookmarks", type_="foreignkey")
    op.create_foreign_key(
        "bookmarks_post_id_fkey",
        "bookmarks",
        "posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("bookmarks_post_id_fkey", "bookmarks", type_="foreignkey")
    op.create_foreign_key(
        "bookmarks_post_id_fkey",
        "bookmarks",
        "posts",
        ["post_id"],
        ["id"],
    )
    op.drop_constraint("post_likes_post_id_fkey", "post_likes", type_="foreignkey")
    op.create_foreign_key(
        "post_likes_post_id_fkey",
        "post_likes",
        "posts",
        ["post_id"],
        ["id"],
    )
