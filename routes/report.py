from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.db import get_db
from db.models import Report as ReportModel
from schemas import ReportCreate, ReportOut

router = APIRouter()


@router.post(
    "/report",
    response_model=ReportOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new incident report",
)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
):
    # Optional: prevent duplicates
    if db.query(ReportModel).filter_by(title=report_in.title).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A report with that title already exists."
        )

    report = ReportModel(**report_in.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get(
    "/report",
    response_model=List[ReportOut],
    summary="Retrieve all incident reports",
)
def read_reports(db: Session = Depends(get_db)):
    return db.query(ReportModel).all()


@router.delete(
    "/report/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an incident report by ID",
)
def delete_report(id: int, db: Session = Depends(get_db)):
    # Use Session.get() instead of the deprecated query.get()
    report = db.get(ReportModel, id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with id={id} not found."
        )
    db.delete(report)
    db.commit()
    return {"ok": True, "message": f"Report {id} deleted"}
