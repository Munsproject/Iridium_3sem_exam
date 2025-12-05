import requests

# TODO: Skift til http://localhost:5000 hvis du vil ramme Flask direkte
BASE_URL = "https://localhost"


def test_create_message_sos():
    """CREATE: Opret en SOS-besked via API'et."""
    payload = {
        "msg_type": "SOS",
        "lat": 55.0,
        "lon": 12.0,
    }
    resp = requests.post(f"{BASE_URL}/messages", json=payload, verify=False)
    assert resp.status_code in (200, 201)

    data = resp.json()
    assert data["msg_type"] == "SOS"
    assert "id" in data

    # Gem id globalt til næste test (pytest kører normalt nyt process, så dette er mest demo)
    global CREATED_ID
    CREATED_ID = data["id"]


def test_read_message_by_id():
    """READ: Læs besked tilbage pr. id."""
    resp = requests.get(f"{BASE_URL}/messages/{CREATED_ID}", verify=False)
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == CREATED_ID
    assert data["msg_type"] == "SOS"


def test_list_messages():
    """READ: Liste alle beskeder og sikre at den oprettede findes."""
    resp = requests.get(f"{BASE_URL}/messages", verify=False)
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)

    ids = [m["id"] for m in data]
    assert CREATED_ID in ids
