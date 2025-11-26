from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
import time

app = FastAPI(title="Events API", version="1.0")

# In-memory store (replace with DB in production)
EVENTS_STORE = {}

class EventIn(BaseModel):
    title: str
    description: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict] = {}

class EventOut(EventIn):
    id: str

# Prometheus metrics
REQ_COUNT = Counter("events_api_requests_total", "Total API requests", ["method","endpoint","http_status"])
REQ_LATENCY = Histogram("events_api_request_latency_seconds", "Request latency seconds", ["endpoint"])

@app.post("/api/v1/events", status_code=201, response_model=EventOut)
async def create_event(event: EventIn, request: Request):
    start = time.time()
    eid = str(uuid4())
    payload = event.dict()
    payload["id"] = eid
    payload["timestamp"] = (payload.get("timestamp") or datetime.utcnow()).isoformat()
    EVENTS_STORE[eid] = payload
    REQ_COUNT.labels(method="POST", endpoint="/api/v1/events", http_status="201").inc()
    REQ_LATENCY.labels(endpoint="/api/v1/events").observe(time.time() - start)
    return payload

@app.get("/api/v1/events")
async def list_events(limit: int = 50, offset: int = 0):
    items = list(EVENTS_STORE.values())[offset:offset+limit]
    REQ_COUNT.labels(method="GET", endpoint="/api/v1/events", http_status="200").inc()
    return {"total": len(EVENTS_STORE), "events": items}

@app.get("/api/v1/events/{event_id}")
async def get_event(event_id: str):
    if event_id not in EVENTS_STORE:
        REQ_COUNT.labels(method="GET", endpoint="/api/v1/events/{id}", http_status="404").inc()
        raise HTTPException(404, "Event not found")
    REQ_COUNT.labels(method="GET", endpoint="/api/v1/events/{id}", http_status="200").inc()
    return EVENTS_STORE[event_id]

@app.delete("/api/v1/events/{event_id}")
async def delete_event(event_id: str):
    if event_id not in EVENTS_STORE:
        raise HTTPException(404, "Event not found")
    del EVENTS_STORE[event_id]
    REQ_COUNT.labels(method="DELETE", endpoint="/api/v1/events/{id}", http_status="200").inc()
    return {"message": "deleted"}

# Expose Prometheus metrics on a separate endpoint
@app.get("/metrics")
async def metrics():
    # Using default registry
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
