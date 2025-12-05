from datetime import datetime

# TODO: Ret import/funktionnavn til det, du faktisk har.
# Eksempel: en funktion der bygger payload til API'et.
from client.client_mock import build_message  # tilpas dette


def test_build_message_contains_all_fields():
    """Beskeden fra klienten skal indeholde msg_type, lat, lon og timestamp."""
    lat, lon = 55.0, 12.0
    msg_type = "LKP"

    msg = build_message(msg_type, lat, lon)

    assert msg["msg_type"] == msg_type
    assert msg["lat"] == lat
    assert msg["lon"] == lon
    assert "timestamp" in msg

    # Tjek at timestamp ligner en ISO8601 streng (meget simpel check)
    ts = msg["timestamp"]
    # Hvis dette fejler, er det bare et hint – kan fjernes hvis det generer
    datetime.fromisoformat(ts.replace("Z", "+00:00"))
