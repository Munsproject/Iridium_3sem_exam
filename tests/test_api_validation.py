import json


def test_post_message_valid_sos(client):
    """Gyldig SOS-besked skal give 201 (eller 200 hvis du bruger det)."""
    payload = {
        "msg_type": "SOS",
        "lat": 55.0,
        "lon": 12.0,
    }
    resp = client.post("/messages", json=payload)

    assert resp.status_code in (200, 201)

    data = resp.get_json()
    assert data["msg_type"] == "SOS"
    assert "id" in data


def test_post_message_missing_lat(client):
    """Manglende latitude skal give 400 Bad Request."""
    payload = {
        "msg_type": "SOS",
        "lon": 12.0,
    }
    resp = client.post("/messages", json=payload)

    assert resp.status_code == 400


def test_post_message_invalid_msg_type(client):
    """Forkert msg_type skal afvises."""
    payload = {
        "msg_type": "WRONG",
        "lat": 55.0,
        "lon": 12.0,
    }
    resp = client.post("/messages", json=payload)

    assert resp.status_code == 400
