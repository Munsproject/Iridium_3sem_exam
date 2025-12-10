import pytest
from api.app import db, Device, Msg, Msg_type, Transport
from api.app import upsert_device_from_msg

@pytest.fixture
def app_context():
    """Give a clean DB for unit tests."""
    from api.app import app
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield

def test_upsert_creates_new_device(app_context):
    msg = Msg(
        device_id="D01",
        lat=55,
        lon=12,
        msg="test",
        msg_type=Msg_type.NORMAL,
        transport=Transport.TCP
    )

    upsert_device_from_msg(msg)
    db.session.commit()

    dev = Device.query.get("D01")
    assert dev is not None
    assert float(dev.last_lat) == 55
    assert float(dev.last_lon) == 12

def test_upsert_updates_existing_device(app_context):
    d = Device(id="D02")
    db.session.add(d)
    db.session.commit()

    msg = Msg(
        device_id="D02",
        lat=60,
        lon=10,
        msg="test",
        msg_type=Msg_type.LKP,
        transport=Transport.TCP
    )

    upsert_device_from_msg(msg)
    db.session.commit()

    dev = Device.query.get("D02")
    assert float(dev.last_lat) == 60
    assert float(dev.last_lon) == 10
    assert dev.last_msg_type == Msg_type.LKP
