from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ParkingLotBase(BaseModel):
    name: str
    address: str
    is_small_lot: bool = False
    hourly_price: float
    website: Optional[str] = None
    slot_count: int
    occupied_count: int = 0
    latitude: float
    longitude: float


class ParkingLotCreate(ParkingLotBase):
    pass


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    is_small_lot: Optional[bool] = None
    hourly_price: Optional[float] = None
    website: Optional[str] = None
    slot_count: Optional[int] = None
    occupied_count: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ParkingLotResponse(ParkingLotBase):
    id: int
    last_updated: Optional[datetime] = None
    available_count: int = 0

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, lot):
        return cls(
            id=lot.id,
            name=lot.name,
            address=lot.address,
            is_small_lot=lot.is_small_lot,
            hourly_price=lot.hourly_price,
            website=lot.website,
            slot_count=lot.slot_count,
            occupied_count=lot.occupied_count,
            latitude=lot.latitude,
            longitude=lot.longitude,
            last_updated=lot.last_updated,
            available_count=lot.slot_count - lot.occupied_count,
        )
