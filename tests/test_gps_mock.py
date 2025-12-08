from math import sin, cos

class GpsMock:
    def __init__(self):
        self.i = 0

    def get_position(self):
        self.i += 1
        return 55.0 + sin(self.i)/10000, 12.0 + cos(self.i)/10000


def test_gps_mock_moves():
    gps = GpsMock()
    p1 = gps.get_position()
    p2 = gps.get_position()

    assert p1 != p2
