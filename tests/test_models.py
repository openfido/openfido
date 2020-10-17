from app.models import db, User
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
