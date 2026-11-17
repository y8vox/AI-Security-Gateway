import os
import sqlite3
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "gateway.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        request_id TEXT NOT NULL,
        prompt TEXT NOT NULL,
        decision TEXT NOT NULL,
        risk_score REAL NOT NULL,
        threats TEXT NOT NULL,
        ml_label TEXT,
        ml_probability REAL,
        latency_ms REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def insert_event(event):
    conn = get_conn()
    conn.execute("""
      INSERT INTO events(timestamp, request_id, prompt, decision, risk_score, threats, ml_label, ml_probability, latency_ms)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(), event["request_id"], event["prompt"],
        event["decision"], event["risk_score"], ",".join(event["threats"]),
        event.get("ml_label"), event.get("ml_probability"), event["latency_ms"]
    ))
    conn.commit()
    conn.close()


def recent_events(limit=50):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def summary():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) c FROM events").fetchone()["c"]
    blocked = conn.execute("SELECT COUNT(*) c FROM events WHERE decision='BLOCK'").fetchone()["c"]
    allowed = conn.execute("SELECT COUNT(*) c FROM events WHERE decision='ALLOW'").fetchone()["c"]
    avg_latency = conn.execute("SELECT COALESCE(AVG(latency_ms),0) v FROM events").fetchone()["v"]
    conn.close()
    return {"total": total, "blocked": blocked, "allowed": allowed, "avg_latency_ms": round(avg_latency, 2)}
