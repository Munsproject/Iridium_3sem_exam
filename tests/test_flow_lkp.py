def test_flow_lkp_multiple_points(client):
    coords = [
        (55.000001, 12.000001),
        (55.000010, 12.000020),
        (55.000020, 12.000030)
    ]

    for lat, lon in coords:
        payload = {
            "device_id": "DEV100",
            "msg_type": "LKP",
            "lat": lat,
            "lon": lon,
            "msg": "periodic LKP update",
            "transport": "tcp"
        }
        resp = client.post("/messages", json=payload)
        assert resp.status_code == 201

    resp = client.get("/api/messages")
    data = resp.get_json()

    returned_coords = {(float(d["lat"]), float(d["lon"])) for d in data}
    for c in coords:
        assert c in returned_coords
