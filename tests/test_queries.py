from app.models import OrganizationInvitation, db
from app import queries
from app import services


def test_find_user_by_email(user):
    # When there is no matching user:
    assert queries.find_user_by_email(None) is None
    assert queries.find_user_by_email("a_user@example.com") is None
    assert queries.find_user_by_email("nonuser@example.com") is None

    # When there is:
    assert queries.find_user_by_email(user.email) == user
