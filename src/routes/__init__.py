from fastapi import APIRouter

from src.routes import auth, user, appointment, patient, dentist, billing, availability, insurance, reports, \
    notifications, feedback

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(user.router, prefix="/user")
router.include_router(appointment.router, prefix="/appointment")
router.include_router(patient.router, prefix="/patient")
router.include_router(dentist.router, prefix="/dentist")
router.include_router(billing.router, prefix="/billing")
router.include_router(availability.router, prefix="/availability")
router.include_router(insurance.router, prefix="/insurance")
router.include_router(reports.router, prefix="/reports")
router.include_router(notifications.router, prefix="/notifications")
router.include_router(feedback.router, prefix="/feedback")
