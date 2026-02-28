"""
Kubernetes Probes Demo Application
===================================
A minimal Flask app demonstrating /healthz (liveness) and /readyz (readiness) endpoints.

Endpoints:
  GET /          — App info
  GET /healthz   — Liveness probe endpoint
  GET /readyz    — Readiness probe endpoint
  POST /kill     — Simulate liveness failure (demo only)
  POST /reset    — Reset to healthy state (demo only)
"""

import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# === State (demo-only — do not use globals in real prod apps) ===
_alive = True
_start_time = time.time()
_startup_delay = 10  # Simulate 10s warm-up for readiness


@app.route("/")
def index():
    elapsed = time.time() - _start_time
    return jsonify({
        "app": "k8s-probes-demo",
        "version": "1.0.0",
        "uptime_seconds": round(elapsed, 1),
        "liveness": "ok" if _alive else "failing",
        "readiness": "ok" if elapsed >= _startup_delay else f"warming up ({round(elapsed,1)}s/{_startup_delay}s)",
    })


@app.route("/healthz")
def healthz():
    """
    LIVENESS endpoint.
    Returns 200 if the app is alive and functioning.
    Returns 500 if the app is in a failed/deadlocked state.

    ✅ Keep this LIGHTWEIGHT — no external calls, no DB checks.
    """
    if not _alive:
        return jsonify({
            "status": "error",
            "message": "App is in a failed state. Pod will restart.",
        }), 500

    return jsonify({
        "status": "ok",
        "uptime_seconds": round(time.time() - _start_time, 1),
    }), 200


@app.route("/readyz")
def readyz():
    """
    READINESS endpoint.
    Returns 200 only when the app is fully ready to serve traffic.
    Returns 503 during startup warmup or when dependencies are unavailable.

    ✅ This CAN check external dependencies (DB, cache, etc.)
    """
    elapsed = time.time() - _start_time

    # Simulate startup warmup (e.g., cache loading, DB pool init)
    if elapsed < _startup_delay:
        return jsonify({
            "status": "not_ready",
            "reason": "warming_up",
            "elapsed_seconds": round(elapsed, 1),
            "startup_delay_seconds": _startup_delay,
            "message": f"App is warming up. Ready in ~{round(_startup_delay - elapsed, 0)}s",
        }), 503

    # In a real app, check dependencies here:
    # - Database connection: db.ping()
    # - Cache availability: redis.ping()
    # - External API: requests.get(config.external_api + "/health")

    return jsonify({
        "status": "ok",
        "message": "App is ready to serve traffic.",
        "checks": {
            "startup": "passed",
            "database": "ok (simulated)",
            "cache": "ok (simulated)",
        },
    }), 200


# === Demo-only endpoints (remove in real production) ===

@app.route("/kill", methods=["POST", "GET"])
def kill():
    """Simulate a liveness failure — Kubernetes will restart this pod."""
    global _alive
    _alive = False
    return jsonify({
        "message": "Liveness probe will now fail!",
        "action": "Pod will be restarted by Kubernetes after failureThreshold is exceeded.",
        "watch": "kubectl get pods -w",
    }), 200


@app.route("/reset", methods=["POST", "GET"])
def reset():
    """Reset to healthy state (for demo reset without pod restart)."""
    global _alive
    _alive = True
    return jsonify({"message": "App reset to healthy state."}), 200


if __name__ == "__main__":
    print(f"[demo] Starting k8s-probes-demo app...")
    print(f"[demo] Liveness endpoint: GET /healthz")
    print(f"[demo] Readiness endpoint: GET /readyz (warm-up: {_startup_delay}s)")
    print(f"[demo] Kill endpoint:      GET /kill  (triggers liveness failure)")
    app.run(host="0.0.0.0", port=8080, debug=False)
