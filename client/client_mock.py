import time
from gps_mock import Narvik
from api_client import send_SOS, send_lkp

def simulate_lkp_every_20min_and_sos(
    lkp_interval_sec=20 * 60,   # 20 minutter i "virkelighed"
    step_delay_sec=2,          # Langsom skridt hatsighed for tests skyld
    sos_after_minutes=60        # hvornår der "sker en ulykke"
):

    gps = Narvik()

    print("[SIM] Enhed er slukket. Startposition (Narvik):")
    lat, lon = gps.get_position()
    print(f"      {lat:.6f}, {lon:.6f}")

    # 1) Enhed tændes
    print("\n[SIM] Enhed tændes (power_on). Vandring + LKP starter...")
    gps.power_on()

    start_time = time.time()
    last_lkp_time = start_time
    sos_after_sec = sos_after_minutes * 60

    while True:
        # Bevæg enheden ét skridt (hvis tændt og ikke frossen)
        lat, lon = gps.get_position()
        now = time.time()

        print(f"[SIM] Går: {lat:.6f}, {lon:.6f}")

        # 2) Send LKP hver lkp_interval_sec
        if now - last_lkp_time >= lkp_interval_sec:
            print("[SIM] LKP-interval nået. Sender LKP")
            send_lkp(lat, lon, text="Periodisk LKP fra enhed")
            last_lkp_time = now

        # 3) Efter sos_after_minutes, SOS + stop bevægelse
        if now - start_time >= sos_after_sec:
            print("\n[SIM] SOS, stopper bevægelse.")
            gps.stop_movement()

            # Frys den sidste position og send SOS
            lat, lon = gps.get_position()
            print(f"[SIM] SOS position (frosset): {lat:.6f}, {lon:.6f}")
            send_SOS(lat, lon, text="SOS i Narvik-fjeldene")
            break

        time.sleep(step_delay_sec)

    # 4) Demonstrér at enheden ikke bevæger sig efter SOS
    print("\n[SIM] Tjekker at positionen er låst efter SOS:")
    for i in range(3):
        lat2, lon2 = gps.get_position()
        print(f"[SIM] Efter-SOS check {i+1}: {lat2:.6f}, {lon2:.6f}")
        time.sleep(step_delay_sec)

if __name__ == "__main__":
    print("[SIM] Starter Narvik-simulation med periodisk LKP + SOS\n")
    simulate_lkp_every_20min_and_sos(
        lkp_interval_sec=20,      # TEST: 20 sek i stedet for 20 min
        step_delay_sec=2,         # ét skridt hvert 2. sekund
        sos_after_minutes=2       # SOS efter ca. 2 minutter
    )

    print("\n[SIM] simulation Færdig")

