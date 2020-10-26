from app.models import db, User, OrganizationRole, OrganizationMember
from freezegun import freeze_time
import datetime


@freeze_time("2020-05-10")
def test_create_user(app, user):
    """ A new user model does save to the database. """
    user.first_name = "first"
    db.session.add(user)
    db.session.commit()

    assert set(User.query.all()) == set([user])

    assert user.updated_at == datetime.datetime(2020, 5, 10)

    # The representation is from the user details
    assert str(user) == f"<User {user.id}: {user.email}>"


def test_enums(app, organization, user):
    org_role = OrganizationRole(name="name", code=5)
    db.session.add(org_role)
    db.session.commit()
    assert org_role.role_enum() == ("name", "5")

    organization_member = OrganizationMember(
        organization=organization,
        organization_role=org_role,
        user=user,
    )
    db.session.add(organization_member)
    db.session.commit()
    assert organization_member.role_enum() == ("name", "5")
