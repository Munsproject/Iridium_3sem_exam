import requests

# TODO: skift til http hvis nødvendigt
BASE_URL = "https://localhost"


def test_invalid_msg_type_not_stored():
    """
    Scenarie: klienten sender en besked med forkert msg_type.
    Forventning: API svarer med 400, og beskeden ligger ikke i listen.
    """
    payload = {
        "msg_type": "WRONGTYPE",
        "lat": 55.0,
        "lon": 12.0,
    }

    resp = requests.post(f"{BASE_URL}/messages", json=payload, verify=False)
    assert resp.status_code == 400

    # Hent alle beskeder og tjek at WRONGTYPE ikke findes
    resp_all = requests.get(f"{BASE_URL}/messages", verify=False)
    assert resp_all.status_code == 200

    data = resp_all.json()
    msg_types = {m["msg_type"] for m in data}
    assert "WRONGTYPE" not in msg_types
