from enum import Enum


class UserRole(Enum):
    patient = "patient"
    dentist = "dentist"
    admin = "admin"


class AppointmentStatus(Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class TreatmentType(Enum):
    cleaning = "cleaning"
    filling = "filling"
    extraction = "extraction"
    root_canal = "root_canal"


class InsuranceProvider(Enum):
    provider_a = "Provider A"
    provider_b = "Provider B"
    provider_c = "Provider C"
