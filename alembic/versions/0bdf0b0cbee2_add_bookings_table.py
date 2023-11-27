"""add bookings table

Revision ID: 0bdf0b0cbee2
Revises: 1a8b86ca9419
Create Date: 2023-06-29 17:56:08.142223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bdf0b0cbee2'
down_revision = '1a8b86ca9419'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'bookings',
        sa.Column('guid', sa.UUID(), primary_key=True),
        sa.Column('user_guid', sa.UUID(), sa.ForeignKey('users.guid'), nullable=False),
        sa.Column('service_guid', sa.UUID(), sa.ForeignKey('services.guid'), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('number_persons', sa.Integer(), nullable=True),
        sa.Column('user_created', sa.UUID(), sa.ForeignKey('users.guid'), nullable=False),
        sa.Column('user_updated', sa.UUID(), sa.ForeignKey('users.guid'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_unique_constraint('user_service_unique', 'bookings', ['user_guid', 'service_guid'])


def downgrade() -> None:
    op.drop_constraint('user_service_unique', 'bookings', type_='unique')
    op.drop_table('bookings')
