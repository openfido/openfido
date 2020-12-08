import logging
import os

from abc import ABC, abstractmethod
from python_http_client.exceptions import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .utils import log


class MailDriver(ABC):
    @abstractmethod
    def send_organization_invitation_email(self, organization, email, invitation):
        """Send an email to the user notifying them how to change their
        password. The email should include the `reset_token` associated with
        the user"""

    @abstractmethod
    def send_password_reset_email(self, user):
        """Send an email to the user notifying them how to change their
        password. The email should include the `reset_token` associated with
        the user"""


class NullDriver(MailDriver):
    def send_organization_invitation_email(self, organization, email, invitation):
        log(
            f"send_organization_invitation_email: organization {organization.id} email {email} invitation {invitation.id}"
        )
        return True

    def send_password_reset_email(self, user):
        log(f"send_password_reset_email: user {user.id} token {user.reset_token}")
        return True


class SendGridDriver(MailDriver):
    def send_organization_invitation_email(self, organization, email, invitation):
        base_url = os.environ.get("CLIENT_BASE_URL")
        accept_invitation_url = f"{base_url}/accept-invitation?invitation_token={invitation.invitation_token}"

        message = Mail(
            from_email=os.environ.get("SYSTEM_FROM_EMAIL_ADDRESS"), to_emails=email
        )
        message.dynamic_template_data = {
            "accept_invitation_url": accept_invitation_url,
            "organization_name": organization.name,
        }
        message.template_id = os.environ.get(
            "SENDGRID_ORGANIZATION_INVITATION_TEMPLATE_ID"
        )
        try:
            log(f"sendgrid: send_organization_invitation_email {email}")
            sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            sendgrid_client.send(message)
            return True
        except Exception as request_error:
            log(request_error, logging.ERROR)

        return False

    def send_password_reset_email(self, user):
        base_url = os.environ.get("CLIENT_BASE_URL")
        password_reset_url = f"{base_url}/reset-password/{user.reset_token}"

        message = Mail(
            from_email=os.environ.get("SYSTEM_FROM_EMAIL_ADDRESS"), to_emails=user.email
        )
        message.dynamic_template_data = {"password_reset_url": password_reset_url}
        message.template_id = os.environ.get("SENDGRID_PASSWORD_RESET_TEMPLATE_ID")
        try:
            log(f"sendgrid: send_password_reset_email {user.email}")
            sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            sendgrid_client.send(message)
            return True
        except Exception as request_error:
            log(request_error, logging.ERROR)

        return False


def make_driver(name=os.environ.get("EMAIL_DRIVER")):
    if name == "sendgrid":
        return SendGridDriver()

    return NullDriver()
