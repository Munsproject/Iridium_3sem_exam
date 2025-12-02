import socket
import struct
import binascii
import json
import time
from datetime import datetime, timezone

class IridiumSBDClient:
    def __init__(self, server_host="127.0.0.1", server_port=10800, imei="300234010753370"):
        self.server_host = server_host
        self.server_port = server_port
        self.imei = imei

    def crc16(self, data: bytes) -> int:
        """Compute CRC16-CCITT (poly 0x1021, init 0xFFFF)."""
        crc = 0xFFFF
        for b in data:
            crc ^= b << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc

    def send_sbd_message(self, payload: bytes):
        """Send a Mobile-Originated (MO) SBD message."""
        print(f"[INFO] Connecting to Iridium Gateway at {self.server_host}:{self.server_port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_host, self.server_port))

        try:
            header = 0x01
            session_type = 0x01  # 0x01 = MO
            mo_len = len(payload)

            # Build SBD MO packet
            packet = struct.pack(">B15sB", header, self.imei.encode("ascii"), session_type)
            packet += struct.pack(">H", mo_len)
            packet += payload

            crc = self.crc16(packet)
            packet += struct.pack(">H", crc)

            print(f"[DEBUG] Sending MO packet ({len(packet)} bytes): {binascii.hexlify(packet)}")
            sock.sendall(packet)

            # Wait for response
            response = sock.recv(1024)
            print(f"[DEBUG] Received {len(response)} bytes from server: {binascii.hexlify(response)}")

            # Parse response
            if len(response) < 7:
                print("[ERROR] Incomplete response from server.")
                return

            header, mo_status, mt_status, mt_len = struct.unpack(">BBBH", response[:5])
            mt_payload = response[5:5 + mt_len]
            crc_received = struct.unpack(">H", response[5 + mt_len:7 + mt_len])[0]
            crc_calc = self.crc16(response[:5 + mt_len])

            if crc_received != crc_calc:
                print(f"[WARN] CRC mismatch! Received {crc_received:04X}, expected {crc_calc:04X}")
            else:
                print("[INFO] CRC OK")

            print(f"[INFO] Header: {header:02X}, MO Status: {mo_status}, MT Status: {mt_status}, MT Length: {mt_len}")
            if mt_len > 0:
                print(f"[INFO] MT Payload (hex): {binascii.hexlify(mt_payload)}")

        finally:
            sock.close()
            print("[INFO] Connection closed.")

    def send_emergency_message(self, lat: float, lon: float, text: str = "Emergency"):
        """Send an emergency SBD message with location and text."""
        timestamp = int(time.time())
        payload_dict = {
            "type": "emergency",
            "time": timestamp,
            "coords": {"lat": lat, "lon": lon},
            "msg": text,
        }
        payload_json = json.dumps(payload_dict).encode("utf-8")
        self.send_sbd_message(payload_json)

    def send_last_known_position(self, lat: float, lon: float):
        """Send last known position SBD message."""
        timestamp = int(time.time())
        payload = {
            "type": "last_known_position",
            "time": timestamp,
            "coords": {"lat": lat, "lon": lon},
        }
        self.send_sbd_message(json.dumps(payload).encode("utf-8"))



if __name__ == "__main__":
    # Example usage
    client = IridiumSBDClient(server_host="127.0.0.1", server_port=10800)
    message = b"Hello Iridium from Python!"
    client.send_sbd_message(message)
    client.send_emergency_message(55.6761, 12.5683, "Test emergency message")

   
