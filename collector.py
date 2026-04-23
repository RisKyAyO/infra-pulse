"""
Metrics collector - polls system stats every N seconds.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any
import psutil


async def collect_once() -> Dict[str, Any]:
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": cpu,
        "mem_used_mb": round(mem.used / 1_048_576, 1),
        "mem_total_mb": round(mem.total / 1_048_576, 1),
        "mem_percent": mem.percent,
        "disk_used_gb": round(disk.used / 1_073_741_824, 2),
        "disk_total_gb": round(disk.total / 1_073_741_824, 2),
        "disk_percent": disk.percent,
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
    }


async def collection_loop(db, alert_engine):
    from config import POLL_INTERVAL_SEC
    while True:
        try:
            snap = await collect_once()
            await db.insert_snapshot(snap)
            await alert_engine.check(snap)
        except Exception as e:
            print(f"[Collector] {e}")
        await asyncio.sleep(POLL_INTERVAL_SEC)
