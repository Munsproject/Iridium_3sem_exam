import socket
import struct
import threading
import binascii

class IridiumSBDServer:
    def __init__(self, host="0.0.0.0", port=10800):
        self.host = host
        self.port = port
        self.server_sock = None
        self._running = False

    def start(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(5)

        print(f"[INFO] Iridium SBD Gateway emulation server listening on {self.host}:{self.port}")
        self._running = True

        while self._running:
            conn, addr = self.server_sock.accept()
            print(f"[INFO] Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            data = conn.recv(4096)
            if not data:
                return

            print(f"[DEBUG] Received {len(data)} bytes from {addr}")
            print(binascii.hexlify(data))

            # Parse Iridium SBD header
            header = data[0]
            if header != 0x01:
                print("[WARN] Not a valid SBD MO request (wrong header byte).")
                return

            imei = data[1:16].decode("ascii", errors="ignore")
            session_type = data[16]
            mo_len = struct.unpack(">H", data[17:19])[0]
            mo_payload = data[19:19 + mo_len]

            print(f"[INFO] IMEI: {imei}")
            print(f"[INFO] Session Type: {session_type}")
            print(f"[INFO] MO Payload Length: {mo_len}")
            print(f"[INFO] MO Payload (hex): {binascii.hexlify(mo_payload)}")

            # Build response (no MT message ready)
            mo_status = 0  # 0 = OK
            mt_status = 0  # 0 = No MT message
            mt_payload = b""  # No MT data
            mt_len = len(mt_payload)

            response = struct.pack(">BBBH", 0x02, mo_status, mt_status, mt_len) + mt_payload

            # Compute CRC16 over the response (as per Iridium spec)
            crc = self.crc16(response)
            response += struct.pack(">H", crc)

            conn.sendall(response)
            print(f"[INFO] Sent response ({len(response)} bytes) to {addr}")

        except Exception as e:
            print(f"[ERROR] Exception handling {addr}: {e}")
        finally:
            conn.close()

    def crc16(self, data: bytes) -> int:
        """Compute CRC16-CCITT (poly 0x1021, init 0xFFFF)"""
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

    def stop(self):
        self._running = False
        if self.server_sock:
            self.server_sock.close()
            print("[INFO] Server stopped.")

if __name__ == "__main__":
    server = IridiumSBDServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping server...")
        server.stop()
