def test_missing_device_id(client):
    payload = {
        "msg_type": "SOS",
        "lat": 55,
        "lon": 12,
        "msg": "SOS"
    }
    resp = client.post("/messages", json=payload)
    assert resp.status_code == 400


def test_missing_lat_lon(client):
    payload = {
        "device_id": "X1",
        "msg_type": "LKP",
        "msg": "test"
    }
    resp = client.post("/messages", json=payload)

    assert resp.status_code == 400


def test_invalid_transport(client):
    payload = {
        "device_id": "X1",
        "msg_type": "LKP",
        "lat": 55,
        "lon": 12,
        "msg": "test",
        "transport": "WRONG"
    }
    resp = client.post("/messages", json=payload)
    
    assert resp.status_code == 400
