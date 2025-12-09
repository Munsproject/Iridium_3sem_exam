import pytest
from api.app import db, Alert, Message, MsgType, Transport
from api.app import create_alert_for_message

@pytest.fixture
def app_context():
    from api.app import app
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield


def test_alert_created_for_sos(app_context):
    msg = Message(
        device_id="D3",
        lat=1,
        lon=1,
        msg="HELP",
        msg_type=MsgType.SOS,
        transport=Transport.TCP,
    )

    # Gem beskeden i test-databasen først
    db.session.add(msg)
    db.session.flush()  

    # Opret alert på baggrund af beskeden
    create_alert_for_message(msg)
    db.session.commit()

    alerts = Alert.query.all()
    assert len(alerts) == 1
    assert alerts[0].alert_type == MsgType.SOS


def test_no_alert_for_lkp(app_context):
    msg = Message(
        device_id="D4",
        lat=1,
        lon=1,
        msg="test",
        msg_type=MsgType.LKP,
        transport=Transport.TCP,
    )

    db.session.add(msg)
    db.session.flush()  

    create_alert_for_message(msg)
    db.session.commit()

    alerts = Alert.query.all()
    assert len(alerts) == 0

