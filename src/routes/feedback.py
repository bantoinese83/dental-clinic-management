# src/routes/feedback.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Feedback
from src.schemas import FeedbackCreate, Feedback as FeedbackSchema

router = APIRouter()


@router.post("/", response_model=FeedbackSchema, tags=["Feedback"], description="Create feedback for an appointment.")
async def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("/{feedback_id}", response_model=FeedbackSchema, tags=["Feedback"], description="Get feedback by ID.")
async def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return db_feedback


@router.get("/", response_model=list[FeedbackSchema], tags=["Feedback"], description="Get all feedback.")
async def get_all_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).all()
    if not feedbacks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No feedback found")
    return feedbacks


@router.put("/{feedback_id}", response_model=FeedbackSchema, tags=["Feedback"], description="Update feedback.")
async def update_feedback(feedback_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.delete("/{feedback_id}", response_model=dict, tags=["Feedback"], description="Delete feedback.")
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    db.delete(db_feedback)
    db.commit()
    return {"detail": "Feedback deleted successfully"}
