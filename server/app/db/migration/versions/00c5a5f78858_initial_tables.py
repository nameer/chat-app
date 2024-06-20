"""Initial tables

Revision ID: 00c5a5f78858
Revises: 
Create Date: 2024-06-20 06:45:31.396296

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "00c5a5f78858"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "User",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=True),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_table(
        "Chat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("is_group", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["created_by"], ["User.id"]),
    )
    op.create_table(
        "ChatMember",
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["Chat.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["User.id"]),
        sa.PrimaryKeyConstraint("chat_id", "user_id"),
    )
    op.create_table(
        "Message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("is_edited", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["Chat.id"]),
        sa.ForeignKeyConstraint(["sender_id"], ["User.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("Message")
    op.drop_table("ChatMember")
    op.drop_table("Chat")
    op.drop_table("User")
