"""SnapLab educational submissions — accepts reserved lab-only test values."""
import hmac
import os
import re
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, request, Response

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096

DB = os.environ.get("SNAPLAB_DB", "/tmp/snaplab-events.sqlite3")
SITE_ORIGIN = os.environ.get("SITE_ORIGIN", "https://walidoux.github.io")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

# These are public lab examples; none represents an actual service credential.
DEMO_PROFILES = {
    "lab-01": {"email": "demo01@snaplab.test", "password": "FICTIF-LAB-101"},
    "lab-02": {"email": "demo02@snaplab.test", "password": "FICTIF-LAB-202"},
    "lab-03": {"email": "demo03@snaplab.test", "password": "FICTIF-LAB-303"},
}

# Only the reserved .test namespace and an explicitly labelled test code
# can be submitted. Never accept a real password, real domain or arbitrary text.
LAB_EMAIL = re.compile(r"^[a-z][a-z0-9._-]{1,29}@snaplab\.test$", re.ASCII)
LAB_CODE = re.compile(r"^LAB-[A-Z0-9]{4,12}$", re.ASCII)

def connect():
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        kind TEXT NOT NULL,
        demo_profile TEXT,
        demo_email TEXT,
        demo_code TEXT
    )""")
    columns = {row[1] for row in db.execute("PRAGMA table_info(events)")}
    for name in ("demo_profile", "demo_email", "demo_code"):
        if name not in columns:
            db.execute(f"ALTER TABLE events ADD COLUMN {name} TEXT")
    db.commit()
    return db

@app.after_request
def cors(response):
    origin = request.headers.get("Origin")
    if origin == SITE_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = SITE_ORIGIN
        response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/health")
def health():
    return jsonify(status="ok", service="snaplab-events")

@app.route("/api/events", methods=["POST", "OPTIONS"])
def events():
    if request.method == "OPTIONS":
        return Response(status=204)
    if request.headers.get("Origin") != SITE_ORIGIN:
        return jsonify(error="Origine non autorisée"), 403

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or payload.get("event") != "demo_submit":
        return jsonify(error="Événement non autorisé"), 400
    if set(payload) - {"event", "demo_profile", "demo_email", "demo_code"}:
        return jsonify(error="Champs supplémentaires interdits"), 400

    profile_id = payload.get("demo_profile")
    if profile_id is not None and profile_id not in DEMO_PROFILES:
        return jsonify(error="Profil de démonstration inconnu"), 400

    email = payload.get("demo_email")
    code = payload.get("demo_code")
    if email is None and code is None:
        # Legacy clients may still send anonymous lab events.
        pass
    elif (
        not isinstance(email, str)
        or not isinstance(code, str)
        or LAB_EMAIL.fullmatch(email) is None
        or LAB_CODE.fullmatch(code) is None
    ):
        return jsonify(
            error="Utiliser uniquement une adresse @snaplab.test et un code LAB- suivi de 4 à 12 caractères."
        ), 400

    with connect() as db:
        db.execute(
            "INSERT INTO events(created_at,kind,demo_profile,demo_email,demo_code) VALUES(?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), "demo_submit", profile_id, email, code),
        )
    return jsonify(ok=True), 201

@app.route("/api/admin/stats", methods=["GET"])
def stats():
    supplied = request.headers.get("Authorization", "")
    if not ADMIN_TOKEN or not hmac.compare_digest(supplied, "Bearer " + ADMIN_TOKEN):
        return jsonify(error="Non autorisé"), 401

    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        rows = db.execute(
            """SELECT created_at,kind,demo_profile,demo_email,demo_code
               FROM events ORDER BY id DESC LIMIT 30"""
        ).fetchall()
    return jsonify(
        total=total,
        recent=[
            {
                "date": date,
                "type": kind,
                "demo_profile": profile_id,
                "demo_email": email,
                "demo_code": code,
                # Compatibility: only for older, predefined demo events.
                "demo_credentials": DEMO_PROFILES.get(profile_id)
                if email is None and code is None else None,
            }
            for date, kind, profile_id, email, code in rows
        ],
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
