import requests
from datetime import datetime, timezone

API_URL = "http://localhost:5000/api/messages"

def send_SOS(lat, lon, text="SOS"):
    payload = {
        "lat": lat,
        "lon": lon,
        "msg": text,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "msg_type": "SOS",
    }

    print("[DEBUG] Sending to API:", payload)
    r = requests.post(API_URL, json=payload, timeout=5)
    r.raise_for_status()
    print("Response:", r.json())

def send_lkp(lat, lon, text="Last Known Position"):
    payload = {
        "lat": lat,
        "lon": lon,
        "msg": text,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "msg_type": "LKP",
    }

    print("[DEBUG] Sending to API (LKP):", payload)
    r = requests.post(API_URL, json=payload, timeout=5)
    r.raise_for_status()
    print("Response:", r.json())

if __name__ == "__main__":
    if __name__ == "__main__":
        send_SOS(59.376123, 11.568987, "SOS Test")
        send_SOS(54.476543, 10.568111, "SOS Test")
        send_SOS(57.876999, 13.568222, "SOS Test")
        send_lkp(59.123456, 11.987654, "LKP Test")

