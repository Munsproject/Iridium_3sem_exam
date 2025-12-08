import os
import uuid
from datetime import datetime
from enum import Enum
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

class MsgType(str, Enum):
    NORMAL = "NORMAL"
    SOS = "SOS"
    LKP = "LKP"

class Transport(str, Enum):
    TCP = "tcp"
    SATELLITE_MOCK = "satellite_mock"

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    device_id = db.Column(db.String(36), nullable=False)
    msg_type = db.Column(db.Enum(MsgType), nullable=False, default=MsgType.NORMAL)
    lat = db.Column(db.Numeric(9,6), nullable=False)
    lon = db.Column(db.Numeric(9,6), nullable=False)
    msg = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    transport = db.Column(db.Enum(Transport), nullable=False, default=Transport.TCP)

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.String(36), primary_key=True)
    last_lat = db.Column(db.Numeric(9, 6))
    last_lon = db.Column(db.Numeric(9, 6))
    last_msg_type = db.Column(db.Enum(MsgType))
    last_seen = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    device_id = db.Column(db.String(36), nullable=False)
    msg_id = db.Column(db.String(36), nullable=False)

    alert_type = db.Column(db.Enum(MsgType), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="CRITICAL")

    message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resolved = db.Column(db.Boolean, default=False, nullable=False)

def upsert_device_from_message(message: Message) -> None:
    """Opret eller opdater Device baseret på en ny besked."""
    device = Device.query.filter_by(id=message.device_id).first()

    if device is None:
        device = Device(
            id=message.device_id,
        )
        db.session.add(device)

    device.last_lat = message.lat
    device.last_lon = message.lon
    device.last_msg_type = message.msg_type
    device.last_seen = message.timestamp


def create_alert_for_message(message: Message) -> None:
    """Opret alert for SOS-beskeder. LKP/NORMAL giver ingen alert."""
    if message.msg_type != MsgType.SOS:
        return  # kun SOS er en kritisk alarm

    alert = Alert(
        device_id=message.device_id,
        msg_id=message.id,
        alert_type=message.msg_type,  # SOS
        message=message.msg,
        severity="CRITICAL",
    )
    db.session.add(alert)

# API running check
@app.route("/")
def index():
    return "Iridium API is running"

# HEALTH CHECK
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# POST: Modtag data fra Iridium-serveren
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json(force=True)

    device_id = data.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    # msg_type: NORMAL, SOS, LKP
    raw_msg_type = data.get("msg_type", "NORMAL")
    try:
        msg_type = MsgType(raw_msg_type)
    except ValueError:
        return jsonify({"error": f"invalid msg_type '{raw_msg_type}'"}), 400

    msg_text = data.get("msg", "")

    lat = data.get("lat")
    lon = data.get("lon")
    if lat is None or lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    raw_transport = data.get("transport", "tcp")
    try:
        transport = Transport(raw_transport)
    except ValueError:
        return jsonify({"error": f"invalid transport '{raw_transport}'"}), 400

    # opret besked
    message = Message(
        device_id=device_id,
        msg_type=msg_type,
        lat=lat,
        lon=lon,
        msg=msg_text,
        transport=transport,
    )

    db.session.add(message)
    db.session.flush()  # giver message.id uden commit endnu

    # opdater Device og lav evt. SOS-alert
    upsert_device_from_message(message)
    create_alert_for_message(message)

    db.session.commit()

    return jsonify({"id": message.id}), 201

# GET: Hent alle beskeder
@app.route("/api/messages", methods=["GET"])
def get_all_messages():
    rows = Message.query.all()
    data = [
        {
            "id": m.id,
            "msg_type": m.msg_type,
            "lat": m.lat,
            "lon": m.lon,
            "msg": m.msg,
            "timestamp": m.timestamp
        }
        for m in rows
    ]
    return jsonify(data), 200

# MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
