from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:iri123@mariadb:3306/iridium_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    msg_type = db.Column(db.String(20), nullable=False, default="NORMAL")
    lat = db.Column(db.Numeric(9,6), nullable=False)
    lon = db.Column(db.Numeric(9,6), nullable=False)
    msg = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

# API running check
@app.route("/")
def index():
    return "Iridium API is running"

# HEALTH CHECK
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# POST: Modtag data fra Iridium-serveren
@app.route("/api/messages", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        # Krævede felter
        required = ["lat", "lon", "msg", "timestamp"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field '{field}'"}), 400

        # Valider data
        try:
            lat = float(data["lat"])
            lon = float(data["lon"])
            timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            return jsonify({"error": "Invalid data format"}), 400
        
        msg_type = data.get("msg_type", "NORMAL")

        msg_id = str(uuid.uuid4())
        new_message = Message(
            id=msg_id,
            lat=lat,
            lon=lon,
            msg=data["msg"],
            timestamp=timestamp.isoformat(),
            msg_type=msg_type,
            )
        db.session.add(new_message)
        db.session.commit()

        print(f"[INFO] New message stored: {msg_id} ({msg_type})")
        return jsonify({"status": "stored", "id": msg_id}), 201

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "Internal server error"}), 500

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
