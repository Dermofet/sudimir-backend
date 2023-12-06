"""Create Admin

Revision ID: 183c52b15c5f
Revises: 55e890b2f766
Create Date: 2023-12-06 20:47:36.060674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '183c52b15c5f'
down_revision = '55e890b2f766'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_bookings_guid'), 'bookings', ['guid'], unique=False)

    op.execute("INSERT INTO users (guid, first_name, last_name, password, role, phone, email) VALUES ('7f57aa44-bc91-4453-9eab-c596c5388c09', 'Admin', 'Admin', '$2y$10$SCxu9Sx8bz5CukcaX/0MEeDH5sKjGYACjZPrsCWr4jnEZVT9oKf9e', 'admin', '+79999999999', 'admin@admin.com')")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bookings_guid'), table_name='bookings')

    op.execute("DELETE FROM users WHERE guid = '7f57aa44-bc91-4453-9eab-c596c5388c09'")
    # ### end Alembic commands ###