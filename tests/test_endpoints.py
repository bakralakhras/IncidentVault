from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from main import app
from db.db import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_report():
    payload = {
        "title": "Test Report",
        "description": "This is a test report",
        "severity": "low"
    }
    response = client.post("/report", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Report"
    assert data["description"] == "This is a test report"
    assert data["severity"] == "low"
    assert "id" in data

def test_read_reports():
    response = client.get("/report")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]
