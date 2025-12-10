from datetime import datetime

def build_msg(device_id, msg_type, lat, lon, msg):
    return {
        "device_id": device_id,
        "msg_type": msg_type,
        "lat": lat,
        "lon": lon,
        "msg": msg,
        "transport": "tcp",
        "timestamp": datetime.utcnow().isoformat()
    }


def test_build_msg_containing_all_fields():
    msg = build_msg("D01", "LKP", 55.0, 12.0, "periodic update")

    assert msg["device_id"] == "D01"
    assert msg["msg_type"] == "LKP"
    assert msg["lat"] == 55.0
    assert msg["lon"] == 12.0
    assert msg["msg"] == "periodic update"
    assert msg["transport"] == "tcp"
    assert "timestamp" in msg
    