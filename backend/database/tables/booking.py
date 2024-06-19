import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.database.connection import Base

class Booking(Base):
    __tablename__ = "bookings"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    user_guid = Column(UUID(as_uuid=True), ForeignKey("users.guid"), nullable=False)  # Use "users" table name
    status = Column(String, nullable=False)
    number_persons = Column(Integer, nullable=True)
    datetime = Column(DateTime, nullable=False)

    user_created = Column(UUID(as_uuid=True), ForeignKey("users.guid"), nullable=False)  # Use "users" table name
    user_updated = Column(UUID(as_uuid=True), ForeignKey("users.guid"), nullable=False)  # Use "users" table name

    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user_rel = relationship("User", back_populates="bookings_rel", lazy="joined", uselist=False, foreign_keys=[user_guid])
    user_created_rel = relationship("User", back_populates="created_bookings_rel", lazy="joined", uselist=False,
                                    foreign_keys=[user_created])
    user_updated_rel = relationship("User", back_populates="updated_bookings_rel", lazy="joined", uselist=False,
                                    foreign_keys=[user_updated])