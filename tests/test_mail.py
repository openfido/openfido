from unittest.mock import Mock

from python_http_client.exceptions import BadRequestsError

from app import mail


def test_make_driver_null():
    assert type(mail.make_driver("null")) == mail.NullDriver


def test_make_driver_sendgrid():
    assert isinstance(mail.make_driver("sendgrid"), mail.SendGridDriver)


def test_send_reset_email_nulldriver(user):
    assert mail.make_driver("null").send_reset_email(user)


def test_send_reset_email_sendgrid(user, monkeypatch):
    sendgrid_mock = Mock()
    monkeypatch.setattr(mail, "SendGridAPIClient", lambda x: sendgrid_mock)

    assert mail.make_driver("sendgrid").send_reset_email(user)
    sendgrid_mock.send.assert_called_once()
    message = sendgrid_mock.mock_calls[0][1][0]
    assert message.personalizations[0].dynamic_template_data == {
        "FirstName": user.first_name,
        "LastName": user.last_name,
        "ResetToken": user.reset_token,
    }


def test_send_reset_email_sendgrid_fails(user, monkeypatch):
    sendgrid_mock = Mock()
    sendgrid_mock.send.side_effect = BadRequestsError(Mock())
    monkeypatch.setattr(mail, "SendGridAPIClient", lambda x: sendgrid_mock)

    assert not mail.make_driver("sendgrid").send_reset_email(user)
    sendgrid_mock.send.assert_called_once()
