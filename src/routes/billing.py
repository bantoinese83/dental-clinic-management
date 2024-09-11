# src/routes/billing.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Billing
from src.schemas import BillingCreate, Billing as BillingSchema

router = APIRouter()

@router.post("/", response_model=BillingSchema, tags=["Billing"], description="Create a billing record.")
async def create_billing(billing: BillingCreate, db: Session = Depends(get_db)):
    db_billing = Billing(**billing.dict())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.get("/patient/{patient_id}", response_model=list[BillingSchema], tags=["Billing"],
            description="Get billing records by patient ID.")
async def get_billing_by_patient(patient_id: int, db: Session = Depends(get_db)):
    db_billing = db.query(Billing).filter(Billing.patient_id == patient_id).all()
    if not db_billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing records not found")
    return db_billing

@router.put("/{billing_id}", response_model=BillingSchema, tags=["Billing"],
            description="Update a billing record.")
async def update_billing(billing_id: int, billing: BillingCreate, db: Session = Depends(get_db)):
    db_billing = db.query(Billing).filter(Billing.id == billing_id).first()
    if not db_billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing record not found")
    for key, value in billing.dict().items():
        setattr(db_billing, key, value)
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.delete("/{billing_id}", response_model=dict, tags=["Billing"], description="Delete a billing record.")
async def delete_billing(billing_id: int, db: Session = Depends(get_db)):
    db_billing = db.query(Billing).filter(Billing.id == billing_id).first()
    if not db_billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing record not found")
    db.delete(db_billing)
    db.commit()
    return {"detail": "Billing record deleted successfully"}