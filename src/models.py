from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, Text, Float, Date, Time
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import relationship

from src.constants import UserRole, InsuranceProvider
from src.main import Base

user_role_enum = PGEnum('patient', 'dentist', 'admin', name='userrole', create_type=False)
appointment_status_enum = PGEnum('pending', 'confirmed', 'cancelled', name='appointmentstatus', create_type=False)
treatment_type_enum = PGEnum('cleaning', 'extraction', 'filling', 'whitening', 'root_canal', 'crown', 'bridge',
                             'implant',
                             'braces', 'invisalign', 'dentures', 'bonding', 'sealant', 'night_guard', 'mouth_guard',
                             'fluoride_treatment', 'xray', 'consultation', 'emergency', name='treatmenttype',
                             create_type=False)

insurance_provider_enum = PGEnum('aetna', 'cigna', 'metlife', 'unitedhealthcare', 'guardian', 'humana', 'delta_dental',
                                 'blue_cross_blue_shield', 'ameritas', 'assurant', 'principal', 'lincoln_financial',
                                 'mutual_of_omaha', 'geha', 'carefirst', 'kaiser_permanente', 'dentemax',
                                 'dental_network_of_america',
                                 'dentegra', name='insuranceprovider', create_type=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.patient, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    medical_history = Column(Text, nullable=True)
    insurance_provider = Column(Enum(InsuranceProvider), nullable=True)
    insurance_policy_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    appointments = relationship("Appointment", backref="patient")


class Dentist(Base):
    __tablename__ = "dentists"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    speciality = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    availability = relationship("Availability", backref="dentist")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    appointments = relationship("Appointment", backref="dentist")


class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)  # Use DateTime
    end_time = Column(DateTime, nullable=False)  # Use DateTime


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    date = Column(Date, nullable=False) # Keep this as Date
    time = Column(Time, nullable=False) # Keep this as Time
    status = Column(String, default="pending")
    treatment_type = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Billing(Base):
    __tablename__ = "billing"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    amount_due = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False)
    payment_method = Column(String, nullable=True)
    insurance_claim_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(Enum(InsuranceProvider), nullable=False)
    policy_number = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    report_details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
