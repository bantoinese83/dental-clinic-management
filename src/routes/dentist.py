# src/routes/dentist.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Dentist
from src.schemas import DentistCreate, Dentist as DentistSchema

router = APIRouter()


@router.post("/dentists", response_model=DentistSchema, tags=["Dentists"], description="Create a new dentist.")
async def create_dentist(dentist: DentistCreate, db: Session = Depends(get_db)):
    db_dentist = Dentist(**dentist.dict())
    db.add(db_dentist)
    db.commit()
    db.refresh(db_dentist)
    return db_dentist


@router.get("/dentists/{dentist_id}", response_model=DentistSchema, tags=["Dentists"], description="Get a dentist by ID.")
async def get_dentist(dentist_id: int, db: Session = Depends(get_db)):
    db_dentist = db.query(Dentist).filter(Dentist.id == dentist_id).first()
    if not db_dentist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dentist not found")
    return db_dentist


@router.put("/dentists/{dentist_id}", response_model=DentistSchema, tags=["Dentists"], description="Update a dentist's information.")
async def update_dentist(dentist_id: int, dentist: DentistCreate, db: Session = Depends(get_db)):
    db_dentist = db.query(Dentist).filter(Dentist.id == dentist_id).first()
    if not db_dentist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dentist not found")
    for key, value in dentist.dict().items():
        setattr(db_dentist, key, value)
    db.commit()
    db.refresh(db_dentist)
    return db_dentist


@router.delete("/dentists/{dentist_id}", response_model=dict, tags=["Dentists"], description="Delete a dentist.")
async def delete_dentist(dentist_id: int, db: Session = Depends(get_db)):
    db_dentist = db.query(Dentist).filter(Dentist.id == dentist_id).first()
    if not db_dentist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dentist not found")
    db.delete(db_dentist)
    db.commit()
    return {"detail": "Dentist deleted successfully"}