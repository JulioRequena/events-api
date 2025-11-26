import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_event():
    payload = {"title":"test event", "description":"desc"}
    res = client.post("/api/v1/events", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    eid = body["id"]

    res2 = client.get(f"/api/v1/events/{eid}")
    assert res2.status_code == 200
    data = res2.json()
    assert data["title"] == "test event"

def test_list_events_empty():
    res = client.get("/api/v1/events?limit=5")
    assert res.status_code == 200
    j = res.json()
    assert "events" in j
