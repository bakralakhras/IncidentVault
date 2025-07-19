import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_404_handler():
    r = client.get("/no-such-route")
    assert r.status_code == 404
    assert r.json() == {"detail": "Not Found"}


def test_validation_error_handler():
    r = client.post("/report", json={})
    assert r.status_code == 422
    # must have two missing-field errors
    details = r.json()["detail"]
    assert any(e["loc"][-1] == "title" for e in details)
    assert any(e["loc"][-1] == "description" for e in details)


@pytest.fixture(autouse=True)
def add_error_route(monkeypatch):
    # Dynamically add an error route for testing
    @app.get("/error")
    def error():
        raise RuntimeError("ouch")
    yield


def test_general_exception_handler():
    r = client.get("/error")
    assert r.status_code == 500
    assert r.json() == {"detail": "Internal server error"}
