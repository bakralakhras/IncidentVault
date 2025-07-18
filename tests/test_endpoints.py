# tests/test_report.py

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db import get_db
from db.models import Base
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_create_report_success():
    payload = {
        "title": "Test Report",
        "description": "This is a test report"
    }
    resp = client.post("/report", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert "id" in data
    assert "created_at" in data


def test_create_report_validation_error():
    resp = client.post("/report", json={})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    keys = {err["loc"][-1] for err in detail}
    assert "title" in keys and "description" in keys


def test_create_report_duplicate():
    payload = {"title": "Dup", "description": "desc"}
    r1 = client.post("/report", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/report", json=payload)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "A report with that title already exists."


def test_read_reports_empty():
    resp = client.get("/report")
    assert resp.status_code == 200
    assert resp.json() == []


def test_read_reports_populated():
    client.post("/report", json={"title": "A", "description": "a"})
    client.post("/report", json={"title": "B", "description": "b"})
    resp = client.get("/report")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 2
    titles = {r["title"] for r in data}
    assert titles == {"A", "B"}


def test_delete_report_success():
    r = client.post("/report", json={"title": "ToDel", "description": "x"})
    rid = r.json()["id"]
    resp = client.delete(f"/report/{rid}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True, "message": f"Report {rid} deleted"}
    resp2 = client.delete(f"/report/{rid}")
    assert resp2.status_code == 404


def test_404_handler():
    resp = client.get("/no-such-route")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}


@pytest.fixture(autouse=True)
def add_error_route(monkeypatch):
    from fastapi import FastAPI
    @app.get("/error")
    def error():
        raise RuntimeError("ouch")
    yield

def test_general_exception_handler():
    resp = client.get("/error")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Internal server error"}
