from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ParkingLot
from app.schemas import ParkingLotCreate, ParkingLotUpdate, ParkingLotResponse

router = APIRouter(prefix="/admin/parking", tags=["admin"])


@router.post("", response_model=ParkingLotResponse, status_code=201)
def create_parking_lot(lot_data: ParkingLotCreate, db: Session = Depends(get_db)):
    lot = ParkingLot(**lot_data.model_dump())
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return ParkingLotResponse.from_orm_model(lot)


@router.put("/{lot_id}", response_model=ParkingLotResponse)
def update_parking_lot(lot_id: int, lot_data: ParkingLotUpdate, db: Session = Depends(get_db)):
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    update_fields = lot_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(lot, field, value)
    db.commit()
    db.refresh(lot)
    return ParkingLotResponse.from_orm_model(lot)


@router.delete("/{lot_id}", status_code=204)
def delete_parking_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    db.delete(lot)
    db.commit()
