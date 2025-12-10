def test_create_msg_sos(client):
    payload = {
        "device_id": "TEST001",
        "msg_type": "SOS",
        "lat": 55.000001,
        "lon": 12.000001,
        "msg": "SOS signal",
        "transport": "tcp"
    }

    resp = client.post("/messages", json=payload)
    assert resp.status_code == 201

    data = resp.get_json()
    assert "id" in data
    msg_id = data["id"]

    # Hent den oprettede besked via GET ALL
    resp2 = client.get("/api/messages")
    assert resp2.status_code == 200

    rows = resp2.get_json()
    assert any(m["id"] == msg_id for m in rows)


def test_create_invalid_msg_type(client):
    payload = {
        "device_id": "TEST001",
        "msg_type": "INVALID",
        "lat": 55.0,
        "lon": 12.0,
        "msg": "bad msg"
    }

    resp = client.post("/messages", json=payload)
    assert resp.status_code == 400
