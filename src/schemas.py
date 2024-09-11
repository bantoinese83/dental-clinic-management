from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, constr, confloat
from pydantic.v1 import validator


class UserRole(str, Enum):
    patient = "patient"
    dentist = "dentist"
    admin = "admin"


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class TreatmentType(str, Enum):
    cleaning = "cleaning"
    filling = "filling"
    extraction = "extraction"
    root_canal = "root_canal"


class InsuranceProvider(str, Enum):
    provider_a = "Provider A"
    provider_b = "Provider B"
    provider_c = "Provider C"


# src/schemas.py
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50) = Field(..., description="The username of the user")
    password: constr(min_length=8) = Field(..., description="The password of the user")
    role: UserRole = Field(..., description="The role of the user")  # Add this line


class Token(BaseModel):
    access_token: str = Field(..., description="The access token for authentication")
    token_type: str = Field(default="bearer", description="The type of the token")


class User(BaseModel):
    id: int = Field(..., description="The unique ID of the user")
    username: str = Field(..., description="The username of the user")
    role: UserRole = Field(..., description="The role of the user")

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    date: str = Field(..., description="The date of the appointment in YYYY-MM-DD format")
    time: str = Field(..., description="The time of the appointment in HH:MM format")
    treatment_type: TreatmentType = Field(..., description="The type of treatment for the appointment")


class Appointment(BaseModel):
    id: int = Field(..., description="The unique ID of the appointment")
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    status: AppointmentStatus = Field(default=AppointmentStatus.pending, description="The status of the appointment")
    treatment_type: TreatmentType = Field(..., description="The type of treatment for the appointment")
    notes: Optional[str] = Field(None, description="Additional notes for the appointment")
    cost: Optional[float] = Field(None, description="The cost of the appointment")

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    first_name: str = Field(..., description="The first name of the patient")
    last_name: str = Field(..., description="The last name of the patient")
    email: str = Field(..., description="The email of the patient")
    phone_number: Optional[str] = Field(None, description="The phone number of the patient")
    address: Optional[str] = Field(None, description="The address of the patient")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the patient")
    emergency_contact_name: Optional[str] = Field(None, description="The name of the emergency contact")
    emergency_contact_phone: Optional[str] = Field(None, description="The phone number of the emergency contact")
    medical_history: Optional[str] = Field(None, description="The medical history of the patient")
    insurance_provider: Optional[InsuranceProvider] = Field(None, description="The insurance provider")
    insurance_policy_number: Optional[str] = Field(None, description="The insurance policy number")


class Patient(BaseModel):
    id: int = Field(..., description="The unique ID of the patient")
    first_name: str = Field(..., description="The first name of the patient")
    last_name: str = Field(..., description="The last name of the patient")
    email: str = Field(..., description="The email of the patient")
    phone_number: Optional[str] = Field(None, description="The phone number of the patient")
    address: Optional[str] = Field(None, description="The address of the patient")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the patient")
    emergency_contact_name: Optional[str] = Field(None, description="The name of the emergency contact")
    emergency_contact_phone: Optional[str] = Field(None, description="The phone number of the emergency contact")
    medical_history: Optional[str] = Field(None, description="The medical history of the patient")
    insurance_provider: Optional[InsuranceProvider] = Field(None, description="The insurance provider")
    insurance_policy_number: Optional[str] = Field(None, description="The insurance policy number")

    class Config:
        from_attributes = True


class BillingCreate(BaseModel):
    appointment_id: int = Field(..., description="The ID of the appointment")
    patient_id: int = Field(..., description="The ID of the patient")
    amount_due: float = Field(gt=0, description="Amount due must be greater than 0")
    payment_status: str = Field(..., description="The payment status of the billing")
    payment_method: str = Field(None, description="The payment method used")
    insurance_claim_id: str = Field(None, description="The insurance claim ID")


class Billing(BaseModel):
    id: int = Field(..., description="The unique ID of the billing record")
    appointment_id: int = Field(..., description="The ID of the appointment")
    patient_id: int = Field(..., description="The ID of the patient")
    amount_due: float = Field(..., description="The amount due for the billing")
    payment_status: str = Field(..., description="The payment status of the billing")
    payment_method: str = Field(None, description="The payment method used")
    insurance_claim_id: str = Field(None, description="The insurance claim ID")

    class Config:
        from_attributes = True


class AvailabilityCreate(BaseModel):
    dentist_id: int = Field(..., description="The ID of the dentist")
    day_of_week: str = Field(..., description="The day of the week")
    start_time: str = Field(..., description="The start time of availability in YYYY-MM-DDTHH:MM format")
    end_time: str = Field(..., description="The end time of availability in YYYY-MM-DDTHH:MM format")

    @validator("start_time", "end_time", pre=True)
    def parse_datetime(cls, value):
        return datetime.fromisoformat(value)

    @validator("end_time")
    def check_time_range(cls, end_time, values):
        start_time = values.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("end_time must be after start_time")
        return end_time


class Availability(BaseModel):
    id: int = Field(..., description="The unique ID of the availability record")
    dentist_id: int = Field(..., description="The ID of the dentist")
    day_of_week: str = Field(..., description="The day of the week")

    class Config:
        from_attributes = True


class DentistCreate(BaseModel):
    first_name: str = Field(..., description="The first name of the dentist")
    last_name: str = Field(..., description="The last name of the dentist")
    speciality: Optional[str] = Field("", description="The speciality of the dentist")
    license_number: Optional[str] = Field("", description="The license number of the dentist")


class Dentist(BaseModel):
    id: int = Field(..., description="The unique ID of the dentist")
    first_name: str = Field(..., description="The first name of the dentist")
    last_name: str = Field(..., description="The last name of the dentist")
    speciality: str = Field(None, description="The speciality of the dentist")
    license_number: str = Field(None, description="The license number of the dentist")

    class Config:
        from_attributes = True


class InsuranceCreate(BaseModel):
    provider: InsuranceProvider = Field(..., description="The insurance provider")
    policy_number: str = Field(..., description="The policy number")
    patient_id: int = Field(..., description="The ID of the patient")


class Insurance(BaseModel):
    id: int = Field(..., description="The unique ID of the insurance record")
    provider: InsuranceProvider = Field(..., description="The insurance provider")
    policy_number: str = Field(..., description="The policy number")
    patient_id: int = Field(..., description="The ID of the patient")

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    appointment_id: int = Field(..., description="The ID of the appointment")
    report_details: str = Field(..., description="The details of the report")


class Report(BaseModel):
    id: int = Field(..., description="The unique ID of the report")
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    appointment_id: int = Field(..., description="The ID of the appointment")
    report_details: str = Field(..., description="The details of the report")

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    user_id: int = Field(..., description="The ID of the user")
    message: str = Field(..., description="The notification message")


class Notification(BaseModel):
    id: int = Field(..., description="The unique ID of the notification")
    user_id: int = Field(..., description="The ID of the user")
    message: str = Field(..., description="The notification message")
    is_read: bool = Field(default=False, description="Read status of the notification")

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    appointment_id: int = Field(..., description="The ID of the appointment")
    rating: int = Field(..., description="The rating given by the patient")
    comments: str = Field(None, description="Additional comments")


class Feedback(BaseModel):
    id: int = Field(..., description="The unique ID of the feedback")
    patient_id: int = Field(..., description="The ID of the patient")
    dentist_id: int = Field(..., description="The ID of the dentist")
    appointment_id: int = Field(..., description="The ID of the appointment")
    rating: int = Field(..., description="The rating given by the patient")
    comments: str = Field(None, description="Additional comments")

    class Config:
        from_attributes = True
