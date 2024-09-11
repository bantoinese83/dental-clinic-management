from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.database import get_db
from src.dental_service import create_appointment, get_patient_by_id, get_appointments_by_patient_id
from src.models import User as UserModel, Appointment
from src.schemas import AppointmentCreate, Appointment as AppointmentSchema

router = APIRouter()


@router.post("/dental/appointments", response_model=AppointmentSchema, tags=["Appointments"],
             description="Create a new dental appointment.")
async def create_appointment_route(appointment: AppointmentCreate, current_user: UserModel = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    patient = get_patient_by_id(db=db, patient_id=appointment.patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    db_appointment = create_appointment(db=db, appointment=appointment)
    return db_appointment


@router.get("/dental/patients/{patient_id}/appointments", response_model=list[AppointmentSchema], tags=["Appointments"],
            description="Get all appointments for a specific patient.")
async def get_appointments_by_patient(patient_id: int, current_user: UserModel = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    patient = get_patient_by_id(db=db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    appointments = get_appointments_by_patient_id(db=db, patient_id=patient_id)
    return appointments


@router.get("/dental/appointments/{appointment_id}", response_model=AppointmentSchema, tags=["Appointments"],
            description="Get details of a specific appointment.")
async def get_appointment(appointment_id: int, current_user: UserModel = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


@router.put("/dental/appointments/{appointment_id}", response_model=AppointmentSchema, tags=["Appointments"],
            description="Update a specific appointment.")
async def update_appointment(appointment_id: int, appointment: AppointmentCreate,
                             current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/dental/appointments/{appointment_id}", response_model=dict, tags=["Appointments"],
               description="Delete a specific appointment.")
async def delete_appointment(appointment_id: int, current_user: UserModel = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return {"detail": "Appointment deleted successfully"}
