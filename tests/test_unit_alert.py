import pytest
from api.app import db, Alert, Msg, Msg_type, Transport
from api.app import create_alert_msg

@pytest.fixture
def app_context():
    from api.app import app
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield


def test_alert_created_for_sos(app_context):
    msg = Msg(
        device_id="D03",
        lat=1,
        lon=1,
        msg="SOS test",
        msg_type=Msg_type.SOS,
        transport=Transport.TCP,
    )

    # Gem beskeden i test-databasen først
    db.session.add(msg)
    db.session.flush()  

    # Opret alert på baggrund af beskeden
    create_alert_msg(msg)
    db.session.commit()

    alerts = Alert.query.all()
    assert len(alerts) == 1
    assert alerts[0].alert_type == Msg_type.SOS


def test_no_alert_for_lkp(app_context):
    msg = Msg(
        device_id="D04",
        lat=1,
        lon=1,
        msg="lkp test",
        msg_type=Msg_type.LKP,
        transport=Transport.TCP,
    )

    db.session.add(msg)
    db.session.flush()  

    create_alert_msg(msg)
    db.session.commit()

    alerts = Alert.query.all()
    assert len(alerts) == 0

