from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from pydantic import ConfigDict


class ReportCreate(BaseModel):
    title: str
    description: str
    severity: Literal["low", "mid", "high"] = "low"
    model_config = ConfigDict(populate_by_name=True)


class ReportOut(BaseModel):
    id: int
    title: str
    description: str
    severity: Literal["low", "mid", "high"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
