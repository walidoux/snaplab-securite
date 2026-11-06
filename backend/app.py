import hmac
import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, request, Response

app = Flask(__name__)
DB = os.environ.get("SNAPLAB_DB", "/tmp/snaplab-events.sqlite3")
SITE_ORIGIN = os.environ.get("SITE_ORIGIN", "https://walidoux.github.io")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

# Identifiants STRICTEMENT fictifs, sans aucun compte réel associé.
# Le navigateur n'envoie que l'ID du profil; les valeurs ci-dessous
# sont associées côté serveur uniquement à des ID pré-approuvés.
DEMO_PROFILES = {
    "lab-01": {"email": "demo01@snaplab.test", "password": "FICTIF-LAB-101"},
    "lab-02": {"email": "demo02@snaplab.test", "password": "FICTIF-LAB-202"},
    "lab-03": {"email": "demo03@snaplab.test", "password": "FICTIF-LAB-303"},
}

def connect():
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        kind TEXT NOT NULL,
        demo_profile TEXT
    )""")
    # Préserve les événements déjà créés avant l'ajout des profils fictifs.
    columns = {row[1] for row in db.execute("PRAGMA table_info(events)")}
    if "demo_profile" not in columns:
        db.execute("ALTER TABLE events ADD COLUMN demo_profile TEXT")
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
    # Aucun champ libre (email, mot de passe, etc.) n'est accepté.
    if set(payload) - {"event", "demo_profile"}:
        return jsonify(error="Champs supplémentaires interdits"), 400
    profile_id = payload.get("demo_profile")
    if profile_id is not None and profile_id not in DEMO_PROFILES:
        return jsonify(error="Profil de démonstration inconnu"), 400
    with connect() as db:
        db.execute(
            "INSERT INTO events(created_at,kind,demo_profile) VALUES(?,?,?)",
            (datetime.now(timezone.utc).isoformat(), "demo_submit", profile_id),
        )
    return jsonify(ok=True), 201

@app.route("/api/admin/stats", methods=["GET"])
def stats():
    auth = request.headers.get("Authorization", "")
    if not ADMIN_TOKEN or not hmac.compare_digest(auth, "Bearer " + ADMIN_TOKEN):
        return jsonify(error="Non autorisé"), 401
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        rows = db.execute(
            "SELECT created_at,kind,demo_profile FROM events ORDER BY id DESC LIMIT 30"
        ).fetchall()
    return jsonify(
        total=total,
        recent=[
            {
                "date": d,
                "type": k,
                "demo_profile": profile_id,
                "demo_credentials": DEMO_PROFILES.get(profile_id),
            }
            for d, k, profile_id in rows
        ],
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
