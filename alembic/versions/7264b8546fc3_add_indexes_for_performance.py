"""Add indexes for performance

Revision ID: 7264b8546fc3
Revises: d99c5d385ccd
Create Date: 2025-08-28 21:03:44.118418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7264b8546fc3'
down_revision: Union[str, Sequence[str], None] = 'd99c5d385ccd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add indexes for better query performance."""
    # Add index on username for faster user lookups
    op.create_index('idx_users_username', 'users', ['username'])
    # Add index on user_id in transactions for faster user transaction queries
    op.create_index('idx_transactions_user_id', 'transactions', ['user_id'])
    # Add index on feed_id in transactions for faster feed transaction queries
    op.create_index('idx_transactions_feed_id', 'transactions', ['feed_id'])


def downgrade() -> None:
    """Remove performance indexes."""
    op.drop_index('idx_transactions_feed_id', 'transactions')
    op.drop_index('idx_transactions_user_id', 'transactions')
    op.drop_index('idx_users_username', 'users')
