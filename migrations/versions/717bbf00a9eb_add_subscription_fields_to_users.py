"""Add subscription fields to users

Revision ID: 717bbf00a9eb
Revises: f00cdc46fe8a
Create Date: 2026-02-01 18:51:04.004451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '717bbf00a9eb'
down_revision: Union[str, Sequence[str], None] = 'f00cdc46fe8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("subscription_expires_at", sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column("subscription_tier", sa.String(length=50), nullable=True)
    )


def downgrade():
    op.drop_column("users", "subscription_expires_at")
    op.drop_column("users", "subscription_tier")