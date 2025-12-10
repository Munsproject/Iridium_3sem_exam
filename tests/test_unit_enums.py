import pytest
from api.app import Msg_type, Transport

def test_msgtype_valid():
    assert Msg_type("SOS") == Msg_type.SOS
    assert Msg_type("NORMAL") == Msg_type.NORMAL
    assert Msg_type("LKP") == Msg_type.LKP

def test_msgtype_invalid():
    with pytest.raises(ValueError):
        Msg_type("XYZ")

def test_transport_valid():
    assert Transport("tcp") == Transport.TCP
    assert Transport("satellite_mock") == Transport.SATELLITE_MOCK

def test_transport_invalid():
    with pytest.raises(ValueError):
        Transport("wifi")
