import math
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ParkingLot
from app.schemas import ParkingLotResponse

router = APIRouter(prefix="/parking", tags=["parking"])


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in miles between two coordinates."""
    R = 3958.8  # Earth radius in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@router.get("", response_model=list[ParkingLotResponse])
def list_parking_lots(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_small_lot: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ParkingLot)
    if min_price is not None:
        query = query.filter(ParkingLot.hourly_price >= min_price)
    if max_price is not None:
        query = query.filter(ParkingLot.hourly_price <= max_price)
    if is_small_lot is not None:
        query = query.filter(ParkingLot.is_small_lot == is_small_lot)
    lots = query.all()
    return [ParkingLotResponse.from_orm_model(lot) for lot in lots]


@router.get("/cheapest", response_model=list[ParkingLotResponse])
def cheapest_lots(db: Session = Depends(get_db)):
    lots = db.query(ParkingLot).order_by(ParkingLot.hourly_price.asc()).all()
    return [ParkingLotResponse.from_orm_model(lot) for lot in lots]


@router.get("/small", response_model=list[ParkingLotResponse])
def small_lots(db: Session = Depends(get_db)):
    lots = db.query(ParkingLot).filter(ParkingLot.is_small_lot == True).all()
    return [ParkingLotResponse.from_orm_model(lot) for lot in lots]


@router.get("/nearby", response_model=list[ParkingLotResponse])
def nearby_lots(
    lat: float = Query(...),
    lng: float = Query(...),
    radius: float = Query(default=2.0),
    db: Session = Depends(get_db),
):
    all_lots = db.query(ParkingLot).all()
    nearby = []
    for lot in all_lots:
        dist = haversine(lat, lng, lot.latitude, lot.longitude)
        if dist <= radius:
            resp = ParkingLotResponse.from_orm_model(lot)
            nearby.append((dist, resp))
    nearby.sort(key=lambda x: x[0])
    return [lot for _, lot in nearby]


@router.get("/{lot_id}", response_model=ParkingLotResponse)
def get_parking_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return ParkingLotResponse.from_orm_model(lot)
