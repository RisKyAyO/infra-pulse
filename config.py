"""Configuration for Infra Pulse."""

POLL_INTERVAL_SEC = 5

THRESHOLDS = {
    "cpu_percent": 85.0,
    "mem_percent": 90.0,
    "disk_percent": 95.0,
}

ALERT_WEBHOOK_URL = ""  # Optional Slack/Discord webhook
ALERT_EMAIL = ""         # Optional SMTP alert email
