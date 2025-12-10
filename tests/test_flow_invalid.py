def test_invalid_no_msg(client):
    payload = {
        "device_id": "D01",
        "msg_type": "LKP",
        "lat": 55,
        "lon": 12
    }
    resp = client.post("/messages", json=payload)
    assert resp.status_code == 400
