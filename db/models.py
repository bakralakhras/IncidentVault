from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime

Base= declarative_base()

class Report(Base):
    __tablename__= "incident_report"
    id = Column(Integer, primary_key=True, index=True)
    title= Column(String, unique= False, nullable=False)
    description= Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity= Column(String)