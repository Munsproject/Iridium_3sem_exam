import pytest
from api.app import MsgType, Transport

def test_msgtype_valid():
    assert MsgType("SOS") == MsgType.SOS
    assert MsgType("NORMAL") == MsgType.NORMAL
    assert MsgType("LKP") == MsgType.LKP

def test_msgtype_invalid():
    with pytest.raises(ValueError):
        MsgType("XYZ")

def test_transport_valid():
    assert Transport("tcp") == Transport.TCP
    assert Transport("satellite_mock") == Transport.SATELLITE_MOCK

def test_transport_invalid():
    with pytest.raises(ValueError):
        Transport("wifi")
