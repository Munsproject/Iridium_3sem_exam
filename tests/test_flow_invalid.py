def test_invalid_missing_msg(client):
    payload = {
        "device_id": "D1",
        "msg_type": "LKP",
        "lat": 55,
        "lon": 12
    }
    resp = client.post("/messages", json=payload)
    assert resp.status_code == 400
