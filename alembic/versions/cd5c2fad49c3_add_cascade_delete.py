"""add cascade delete

Revision ID: cd5c2fad49c3
Revises: 23711128ef91
Create Date: 2023-12-12 18:42:15.666562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd5c2fad49c3'
down_revision = '23711128ef91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_foreign_key(
    #     'fk_booking_service',
    #     'bookings',
    #     'services',
    #     ['service_guid'],
    #     ['guid'],
    #     ondelete='CASCADE'  # Каскадное удаление
    # )

    op.create_foreign_key(
        'fk_booking_user',
        'bookings',
        'users',
        ['user_guid'],
        ['guid'],
        ondelete='CASCADE'
    )

    # Добавляем внешний ключ для created_bookings_rel с каскадным удалением
    op.create_foreign_key(
        'fk_created_booking_user',
        'bookings',
        'users',
        ['user_created'],
        ['guid'],
        ondelete='CASCADE'
    )

    # Добавляем внешний ключ для updated_bookings_rel с каскадным удалением
    op.create_foreign_key(
        'fk_updated_booking_user',
        'bookings',
        'users',
        ['user_updated'],
        ['guid'],
        ondelete='CASCADE'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint('fk_booking_service', 'bookings', type_='foreignkey')
    op.drop_constraint('fk_booking_user', 'bookings', type_='foreignkey')
    op.drop_constraint('fk_created_booking_user', 'bookings', type_='foreignkey')
    op.drop_constraint('fk_updated_booking_user', 'bookings', type_='foreignkey')
    # ### end Alembic commands ###
