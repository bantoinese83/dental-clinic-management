# src/routes/availability.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Availability
from src.schemas import AvailabilityCreate, Availability as AvailabilitySchema

router = APIRouter()


@router.post("/", response_model=AvailabilitySchema, tags=["Availability"],
             description="Create availability for a dentist.")
async def create_availability(availability: AvailabilityCreate, db: Session = Depends(get_db)):
    try:
        # Validate that start_time is before end_time
        if availability.start_time >= availability.end_time:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Start time must be before end time")

        db_availability = Availability(**availability.dict())
        db.add(db_availability)
        db.commit()
        db.refresh(db_availability)
        return db_availability
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/{dentist_id}", response_model=list[AvailabilitySchema], tags=["Availability"],
            description="Get availability by dentist ID.")
async def get_availability(dentist_id: int, db: Session = Depends(get_db)):
    db_availability = db.query(Availability).filter(Availability.dentist_id == dentist_id).all()
    if not db_availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability not found")
    return db_availability


@router.put("/{availability_id}", response_model=AvailabilitySchema, tags=["Availability"],
            description="Update availability.")
async def update_availability(availability_id: int, availability: AvailabilityCreate, db: Session = Depends(get_db)):
    db_availability = db.query(Availability).filter(Availability.id == availability_id).first()
    if not db_availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability not found")
    for key, value in availability.dict().items():
        setattr(db_availability, key, value)
    db.commit()
    db.refresh(db_availability)
    return db_availability


@router.delete("/{availability_id}", response_model=dict, tags=["Availability"],
               description="Delete availability.")
async def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    db_availability = db.query(Availability).filter(Availability.id == availability_id).first()
    if not db_availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability not found")
    db.delete(db_availability)
    db.commit()
    return {"detail": "Availability deleted successfully"}
