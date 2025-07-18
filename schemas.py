from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class ReportCreate(BaseModel):
    title: str
    description: str
    severity: Literal["low", "mid", "high"]

class ReportOut(BaseModel):
     id: int
     title: str
     description: str
     severity: Literal["low", "mid", "high"]
     timestamp: datetime
