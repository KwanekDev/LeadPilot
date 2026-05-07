"""remove license management tables and columns

Revision ID: 005
Revises: 004
Create Date: 2026-05-07 00:00:01.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f("ix_licenses_email"), table_name="licenses")
    op.drop_index(op.f("ix_licenses_user_id"), table_name="licenses")
    op.drop_index(op.f("ix_licenses_key_hash"), table_name="licenses")
    op.drop_table("licenses")

    op.drop_index(op.f("ix_users_license_key_hash"), table_name="users")
    op.drop_column("users", "is_license_active")
    op.drop_column("users", "license_key_hash")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("license_key_hash", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("is_license_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index(op.f("ix_users_license_key_hash"), "users", ["license_key_hash"], unique=True)

    op.create_table(
        "licenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key_hash", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_licenses_key_hash"), "licenses", ["key_hash"], unique=True)
    op.create_index(op.f("ix_licenses_user_id"), "licenses", ["user_id"])
    op.create_index(op.f("ix_licenses_email"), "licenses", ["email"])
