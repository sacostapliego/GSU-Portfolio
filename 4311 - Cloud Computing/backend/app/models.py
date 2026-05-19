from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from app.database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_small_lot = Column(Boolean, default=False)
    hourly_price = Column(Float, nullable=False)
    website = Column(String, nullable=True)
    slot_count = Column(Integer, nullable=False)
    occupied_count = Column(Integer, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
