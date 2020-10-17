import logging
import os

from abc import ABC, abstractmethod
from python_http_client.exceptions import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .utils import log


class MailDriver(ABC):
    @abstractmethod
    def send_reset_email(self, user):
        """Send an email to the user notifying them how to change their
        password. The email should include the `reset_token` associated with
        the user"""


class NullDriver(MailDriver):
    def send_reset_email(self, user):
        log(f"send_reset_email: user {user.id} token {user.reset_token}")
        return True


class SendGridDriver(MailDriver):
    def send_password_reset_email(self, user):
        message = Mail(from_email=os.environ.get("SYSTEM_EMAIL"), to_emails=user.email)
        message.dynamic_template_data = {
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "ResetToken": user.reset_token,
        }
        message.template_id = os.environ.get("SENDGRID_PASSWORD_RESET_TEMPLATE_ID")
        try:
            log(f"sendgrid: send_reset_email {user.email}")
            sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            sendgrid_client.send(message)
            return True
        except BadRequestsError as request_error:
            log(request_error, logging.ERROR)

        return False


def make_driver(name=os.environ.get("EMAIL_DRIVER")):
    if name == "sendgrid":
        return SendGridDriver()

    return NullDriver()
