import os
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, request, Response

app = Flask(__name__)
DB = os.environ.get("SNAPLAB_DB", "/tmp/snaplab-events.sqlite3")
SITE_ORIGIN = os.environ.get("SITE_ORIGIN", "https://walidoux.github.io")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

def connect():
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        kind TEXT NOT NULL
    )""")
    db.commit()
    return db

@app.after_request
def cors(resp):
    origin = request.headers.get("Origin")
    if origin == SITE_ORIGIN:
        resp.headers["Access-Control-Allow-Origin"] = SITE_ORIGIN
        resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Cache-Control"] = "no-store"
    return resp

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
    # Aucun champ libre n'est enregistré : ni e-mail, ni mot de passe, ni IP.
    with connect() as db:
        db.execute("INSERT INTO events(created_at,kind) VALUES(?,?)",
                   (datetime.now(timezone.utc).isoformat(), "demo_submit"))
    return jsonify(ok=True), 201

@app.route("/api/admin/stats", methods=["GET"])
def stats():
    if not ADMIN_TOKEN or request.headers.get("Authorization") != "Bearer " + ADMIN_TOKEN:
        return jsonify(error="Non autorisé"), 401
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        rows = db.execute("SELECT created_at,kind FROM events ORDER BY id DESC LIMIT 30").fetchall()
    return jsonify(total=total, recent=[{"date": d, "type": k} for d,k in rows])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
