"""add tenant smtp settings and public lead capture slug

Revision ID: 003
Revises: 002
Create Date: 2026-05-06 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tenants', sa.Column('smtp_server', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('smtp_port', sa.Integer(), nullable=True))
    op.add_column('tenants', sa.Column('smtp_username', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('smtp_password', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('smtp_from_email', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('smtp_tls', sa.Boolean(), nullable=True))
    op.add_column('tenants', sa.Column('lead_capture_slug', sa.String(length=255), nullable=True))
    op.add_column('tenants', sa.Column('lead_capture_enabled', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_tenants_lead_capture_slug'), 'tenants', ['lead_capture_slug'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_tenants_lead_capture_slug'), table_name='tenants')
    op.drop_column('tenants', 'lead_capture_enabled')
    op.drop_column('tenants', 'lead_capture_slug')
    op.drop_column('tenants', 'smtp_tls')
    op.drop_column('tenants', 'smtp_from_email')
    op.drop_column('tenants', 'smtp_password')
    op.drop_column('tenants', 'smtp_username')
    op.drop_column('tenants', 'smtp_port')
    op.drop_column('tenants', 'smtp_server')
