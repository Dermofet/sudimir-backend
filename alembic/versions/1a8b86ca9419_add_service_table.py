"""add service table

Revision ID: 1a8b86ca9419
Revises: eaefcff35784
Create Date: 2023-06-25 21:17:07.531579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a8b86ca9419'
down_revision = 'eaefcff35784'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('services',
    # sa.Column('guid', sa.UUID(), nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.Column('description', sa.Text(), nullable=False),
    # sa.Column('price', sa.Integer(), nullable=False),
    # sa.Column('datetime', sa.DateTime(), nullable=False),
    # sa.Column('duration', sa.String(), nullable=False),
    # sa.Column('max_number_persons', sa.Integer(), nullable=False),
    # sa.Column('type', sa.String(), nullable=False),
    # sa.Column('is_deleted', sa.Boolean(), nullable=True),
    # sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    # sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    # sa.PrimaryKeyConstraint('guid')
    # )
    # op.create_index(op.f('ix_services_guid'), 'services', ['guid'], unique=False)
    # ### end Alembic commands ###
    pass

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index(op.f('ix_services_guid'), table_name='services')
    # op.drop_table('services')
    # ### end Alembic commands ###
    pass