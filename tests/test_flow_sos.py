import requests

# TODO: Tilpas imports til din GPS- og klientkode
from client.gps_mock import Gps_mock
from client.api_client import send_sos  # funktion der sender SOS til API'et

# TODO: Skift til http hvis nødvendigt
BASE_URL = "https://localhost"


def test_flow_sos_freezes_last_position():
    """
    Scenarie: enheden bevæger sig, SOS udløses, og sidste position sendes.
    Vi checker, at SOS-beskeden i DB matcher sidste koord fra GPS'en.
    """
    gps = Gps_mock()

    # Første position (before movement)
    gps.get_position()
    # Anden position: den vil vi bruge til SOS
    lat2, lon2 = gps.get_position()
    lat2r, lon2r = round(lat2, 6), round(lon2, 6)

    # Udløs SOS fra klienten
    send_sos(lat2, lon2)

    # Hent SOS-beskeder fra API
    resp = requests.get(f"{BASE_URL}/messages?msg_type=SOS", verify=False)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0

    # Antag sidste SOS er den nyeste
    data_sorted = sorted(data, key=lambda m: m.get("timestamp", ""))
    last_sos = data_sorted[-1]

    sos_lat = round(float(last_sos["lat"]), 6)
    sos_lon = round(float(last_sos["lon"]), 6)

    assert sos_lat == lat2r
    assert sos_lon == lon2r
