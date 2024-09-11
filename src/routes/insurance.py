from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Insurance
from src.schemas import InsuranceCreate, Insurance as InsuranceSchema

router = APIRouter()


@router.post("/insurances", response_model=InsuranceSchema, tags=["Insurance"], description="Create a new insurance record.")
async def create_insurance(insurance: InsuranceCreate, db: Session = Depends(get_db)):
    db_insurance = Insurance(**insurance.dict())
    db.add(db_insurance)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance


@router.get("/insurances/{insurance_id}", response_model=InsuranceSchema, tags=["Insurance"], description="Get an insurance record by ID.")
async def get_insurance(insurance_id: int, db: Session = Depends(get_db)):
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance record not found")
    return db_insurance


@router.put("/insurances/{insurance_id}", response_model=InsuranceSchema, tags=["Insurance"], description="Update an insurance record.")
async def update_insurance(insurance_id: int, insurance: InsuranceCreate, db: Session = Depends(get_db)):
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance record not found")
    for key, value in insurance.dict().items():
        setattr(db_insurance, key, value)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance


@router.delete("/insurances/{insurance_id}", response_model=dict, tags=["Insurance"], description="Delete an insurance record.")
async def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance record not found")
    db.delete(db_insurance)
    db.commit()
    return {"detail": "Insurance record deleted successfully"}