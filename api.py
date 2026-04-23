"""
FastAPI REST API for Infra Pulse.
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from collector import collection_loop, collect_once
from database import Database
from alerting import AlertEngine
from config import THRESHOLDS

db = Database()
alert_engine = AlertEngine(THRESHOLDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    asyncio.create_task(collection_loop(db, alert_engine))
    yield
    await db.close()


app = FastAPI(title="Infra Pulse API", version="1.0.0", lifespan=lifespan)


@app.get("/metrics/current")
async def current_metrics():
    """Return a live snapshot (bypasses DB)."""
    return await collect_once()


@app.get("/metrics/history")
async def metrics_history(minutes: int = Query(default=60, ge=1, le=1440)):
    """Return historical snapshots for the last N minutes."""
    rows = await db.get_history(minutes=minutes)
    return {"count": len(rows), "data": rows}


@app.get("/metrics/alerts")
async def active_alerts():
    """Return current threshold violations."""
    snapshot = await collect_once()
    violations = await alert_engine.check(snapshot, notify=False)
    return {"alerts": violations}


@app.post("/config/thresholds")
async def update_thresholds(thresholds: dict):
    """Update alert thresholds at runtime."""
    alert_engine.update_thresholds(thresholds)
    return {"message": "Thresholds updated", "thresholds": alert_engine.thresholds}
