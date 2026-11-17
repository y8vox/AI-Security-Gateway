import time
import uuid
from flask import Blueprint, jsonify, request
from .detector import detect
from .database import insert_event, recent_events, summary

api = Blueprint("api", __name__)


def _scan(prompt):
    started = time.perf_counter()
    result = detect(prompt)
    latency = round((time.perf_counter() - started) * 1000, 2)
    result.update({"request_id": str(uuid.uuid4()), "latency_ms": latency, "prompt": prompt})
    insert_event(result)
    return result


@api.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "AI Security Gateway", "version": "1.0.0"})


@api.post("/scan")
def scan():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    return jsonify(_scan(prompt))


@api.post("/gateway")
def gateway():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    result = _scan(prompt)
    if result["decision"] == "BLOCK":
        result["response"] = "Request blocked by AI Security Gateway policy."
        return jsonify(result), 403
    result["response"] = "Request allowed. Mock upstream response generated successfully."
    return jsonify(result)


@api.get("/events")
def events():
    limit = min(int(request.args.get("limit", 50)), 200)
    return jsonify(recent_events(limit))


@api.get("/summary")
def stats():
    return jsonify(summary())


@api.get("/rules")
def rules():
    return jsonify([
        {"name": "SQL Injection", "severity": "Critical", "action": "BLOCK"},
        {"name": "Cross-Site Scripting (XSS)", "severity": "High", "action": "BLOCK"},
        {"name": "Directory Traversal", "severity": "High", "action": "BLOCK"},
        {"name": "Command Injection", "severity": "Critical", "action": "BLOCK"},
        {"name": "Prompt Injection", "severity": "Critical", "action": "BLOCK"},
        {"name": "Credential Exfiltration", "severity": "High", "action": "BLOCK"},
        {"name": "ML Anomaly", "severity": "Medium", "action": "BLOCK when risk >= 70"},
    ])
