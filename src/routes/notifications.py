from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Notification
from src.schemas import NotificationCreate, Notification as NotificationSchema

router = APIRouter()


@router.post("/notifications", response_model=NotificationSchema, tags=["Notifications"], description="Create a new notification.")
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.get("/notifications/{notification_id}", response_model=NotificationSchema, tags=["Notifications"], description="Get a notification by ID.")
async def get_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return db_notification


@router.put("/notifications/{notification_id}", response_model=NotificationSchema, tags=["Notifications"], description="Update a notification.")
async def update_notification(notification_id: int, notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    for key, value in notification.dict().items():
        setattr(db_notification, key, value)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.delete("/notifications/{notification_id}", response_model=dict, tags=["Notifications"], description="Delete a notification.")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return {"detail": "Notification deleted successfully"}