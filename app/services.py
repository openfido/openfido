import requests
from .constants import AUTH_HOSTNAME
from flask import current_app


def fetch_is_user_in_org(organization_uuid, jwt_token, user_uuid):
    """ Verify user_uuid is a member of organization_uuid by calling AUTH_HOSTNAME API. """
    # TODO exception?
    response = requests.get(
        f"{current_app.config[AUTH_HOSTNAME]}/users/{user_uuid}/organizations",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {jwt_token}"
                 },
        json={"uuid": user_uuid}
    )
    response.raise_for_status()

    return organization_uuid in [org["uuid"] for org in response.json()]
