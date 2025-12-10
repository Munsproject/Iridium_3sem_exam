def test_flow_sos_creates_alert_and_update(client):
    lat = 55.123456
    lon = 12.654321

    payload = {
        "device_id": "SOS_DEV",
        "msg_type": "SOS",
        "lat": lat,
        "lon": lon,
        "msg": "SOS emergency",
        "transport": "tcp"
    }

    resp = client.post("/messages", json=payload)
    assert resp.status_code == 201

    resp2 = client.get("/api/messages")
    rows = resp2.get_json()

    sos_msg = next(m for m in rows if m["msg_type"] == "SOS")

    assert float(sos_msg["lat"]) == lat
    assert float(sos_msg["lon"]) == lon

