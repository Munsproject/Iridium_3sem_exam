from datetime import datetime

def build_message(device_id, msg_type, lat, lon, msg):
    return {
        "device_id": device_id,
        "msg_type": msg_type,
        "lat": lat,
        "lon": lon,
        "msg": msg,
        "transport": "tcp",
        "timestamp": datetime.utcnow().isoformat()
    }


def test_build_message_contains_all_fields():
    msg = build_message("D1", "LKP", 55.0, 12.0, "periodic update")

    assert msg["device_id"] == "D1"
    assert msg["msg_type"] == "LKP"
    assert msg["lat"] == 55.0
    assert msg["lon"] == 12.0
    assert msg["msg"] == "periodic update"
    assert msg["transport"] == "tcp"
    assert "timestamp" in msg
