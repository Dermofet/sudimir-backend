# import uuid
# from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from backend.database.connection import Base


# class Service(Base):
#     __tablename__ = "services"

#     guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=False)
#     price = Column(Integer, nullable=False)
#     datetime = Column(DateTime, nullable=False)
#     duration = Column(String, nullable=False)
#     max_number_persons = Column(Integer, nullable=False)
#     type = Column(String, nullable=False)

#     is_deleted = Column(Boolean, default=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

#     bookings_rel = relationship("Booking", back_populates="service_rel", lazy="joined", uselist=True, cascade="all, delete-orphan")