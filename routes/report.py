from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db import SessionLocal
from db.models import Report
from typing import List
from schemas import ReportOut
from schemas import ReportCreate
from fastapi import HTTPException
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/report")
def create_report(payload:ReportCreate, db: Session = Depends(get_db)):
    new_report=Report(**payload.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
@router.get("/report", response_model=List[ReportOut])
def read_reports(db: Session = Depends(get_db)):
    reports= db.query(Report).all()
    return reports
    
@router.delete("/report/{id}")
def delete_report(id: int, db: Session = Depends(get_db)):
    entry= db.query(Report).get(id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    db.delete(entry)
    db.commit()
    return {"ok": True, "message": f"Report {id} deleted"}

