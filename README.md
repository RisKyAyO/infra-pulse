# Infra Pulse

A **lightweight infrastructure monitoring dashboard** that tracks system health metrics in real-time and exposes them via a REST API and a clean web UI. Fully containerised with Docker.

## Features

- Real-time CPU, RAM, disk and network metrics
- REST API (FastAPI) for programmatic access
- Configurable threshold alerts
- One-command deployment with Docker Compose
- Metrics history stored in SQLite

## Stack

| Layer | Technology |
|---|---|
| Metrics collection | psutil |
| API | FastAPI + Uvicorn |
| Database | SQLite (aiosqlite) |
| Containerisation | Docker + Docker Compose |

## Quick Start

```bash
git clone https://github.com/RisKyAyO/infra-pulse
cd infra-pulse
docker compose up -d
```

API docs: `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /metrics/current | Live snapshot |
| GET | /metrics/history?minutes=60 | Historical data |
| GET | /metrics/alerts | Active threshold alerts |
| POST | /config/thresholds | Update alert thresholds |

## Architecture

```
[psutil collector] -> [FastAPI backend] -> [SQLite history]
                             |
                    [REST API / WebSocket]
                             |
                    [Chart.js Dashboard]
```

## Roadmap

- [ ] Prometheus metrics endpoint
- [ ] Grafana dashboard template
- [ ] Multi-node topology view
- [ ] Kubernetes pod monitoring

## License

MIT
