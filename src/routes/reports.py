from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Report
from src.schemas import ReportCreate, Report as ReportSchema

router = APIRouter()


@router.post("/reports", response_model=ReportSchema, tags=["Reports"], description="Create a new report.")
async def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.get("/reports/{report_id}", response_model=ReportSchema, tags=["Reports"], description="Get a report by ID.")
async def get_report(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return db_report


@router.put("/reports/{report_id}", response_model=ReportSchema, tags=["Reports"], description="Update a report.")
async def update_report(report_id: int, report: ReportCreate, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    for key, value in report.dict().items():
        setattr(db_report, key, value)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.delete("/reports/{report_id}", response_model=dict, tags=["Reports"], description="Delete a report.")
async def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    db.delete(db_report)
    db.commit()
    return {"detail": "Report deleted successfully"}