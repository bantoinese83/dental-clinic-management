from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Patient
from src.schemas import PatientCreate, Patient as PatientSchema

router = APIRouter()


@router.post("/patients", response_model=PatientSchema, tags=["Patients"], description="Create a new patient.")
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(first_name=patient.first_name, last_name=patient.last_name, email=patient.email)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("/patients/{patient_id}", response_model=PatientSchema, tags=["Patients"],
            description="Get a patient by ID.")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.put("/patients/{patient_id}", response_model=PatientSchema, tags=["Patients"], description="Update a patient.")
async def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/patients/{patient_id}", response_model=dict, tags=["Patients"], description="Delete a patient.")
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
