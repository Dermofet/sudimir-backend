import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.database.connection import Base

class User(Base):
    __tablename__ = "users"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    middle_name = Column(String(50), nullable=True)
    password = Column(String, nullable=True)

    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    role = Column(String, nullable=False)

    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    bookings_rel = relationship("Booking", back_populates="user_rel", lazy="joined", uselist=True,
                                foreign_keys='Booking.user_guid')
    created_bookings_rel = relationship("Booking", back_populates="user_created_rel", lazy="joined", uselist=True,
                                        foreign_keys='Booking.user_created')
    updated_bookings_rel = relationship("Booking", back_populates="user_updated_rel", lazy="joined", uselist=True,
                                        foreign_keys='Booking.user_updated')
