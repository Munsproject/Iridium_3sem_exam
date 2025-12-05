import time
import requests

# TODO: Tilpas imports til din rigtige GPS- og klientkode
from client.gps_mock import Gps_mock
from client.api_client import send_lkp  # du skal have en funktion, der POST'er til API'et

# TODO: Skift til http://localhost:5000 hvis du ikke bruger Nginx/HTTPS
BASE_URL = "https://localhost"


def test_flow_lkp_multiple_points():
    """
    Scenarie: enheden tændes, går nogle "skridt" og sender flere LKP.
    Vi checker, at disse LKP findes i databasen bagefter.
    """
    gps = Gps_mock()
    coords_sent = []

    # Send fx 3 LKP
    for _ in range(3):
        lat, lon = gps.get_position()
        coords_sent.append((round(lat, 6), round(lon, 6)))
        send_lkp(lat, lon)  # denne funktion skal lave POST til /messages med msg_type=LKP
        time.sleep(0.5)  # kort delay i test

    # Hent alle LKP-beskeder
    resp = requests.get(f"{BASE_URL}/messages?msg_type=LKP", verify=False)
    assert resp.status_code == 200
    data = resp.json()

    lkp_coords = [
        (round(float(m["lat"]), 6), round(float(m["lon"]), 6))
        for m in data
        if m["msg_type"] == "LKP"
    ]

    for c in coords_sent:
        assert c in lkp_coords
