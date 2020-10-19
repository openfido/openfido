from datetime import datetime, timezone

import jwt
from freezegun import freeze_time
from unittest.mock import patch
from app import utils

A_PASSWORD = "apassword!"


def test_hashing():
    # Encrypted password generate different hashes/salts every time
    hashed_pw, salt = utils.make_hash(A_PASSWORD)
    hashed_pw2, salt2 = utils.make_hash(A_PASSWORD)
    assert hashed_pw != hashed_pw2
    assert salt != salt2

    # Both hashes are valid
    assert utils.verify_hash(A_PASSWORD, hashed_pw, salt)
    assert utils.verify_hash(A_PASSWORD, hashed_pw2, salt2)

    # Mixed hashes are not valid:
    assert not utils.verify_hash(A_PASSWORD, hashed_pw2, salt)

    # Strings are acceptable parameters
    assert utils.verify_hash(A_PASSWORD, hashed_pw2, salt2)


@freeze_time("2020-04-01")
def test_decode_jwt(app, user):
    # A generated token can be decoded
    a_jwt = utils.make_jwt(user)
    decoded_jwt = utils.decode_jwt(a_jwt.decode("utf-8"))
    assert decoded_jwt["uuid"] == user.uuid
    assert set(decoded_jwt.keys()) == set(["uuid", "exp", "iat", "iss", "max-exp"])

    # A blank string cannot be decoded
    assert not utils.decode_jwt("")

    # A random string cannot be decoded
    assert not utils.decode_jwt("aoeucenet")

    # A jwt without an id key is not valid:
    a_jwt = jwt.encode(
        {},
        app.config["SECRET_KEY"],
        algorithm=utils.JWT_ALGORITHM,
    )
    assert not utils.decode_jwt(a_jwt.decode("utf-8"))

    # A jwt with an expired max-exp can be decoded
    a_jwt = utils.make_jwt(user)
    with freeze_time("2020-04-02"):
        assert utils.decode_jwt(a_jwt.decode("utf-8")) is not False


@freeze_time("2020-04-01")
def test_generate_jwt(app, user):
    # A JWT token is generated for a user and is verifiable
    SECRET_KEY = app.config["SECRET_KEY"]
    a_jwt = utils.make_jwt(user)

    # A JWT token will differ over time:
    with freeze_time("2020-04-02"):
        decoded_jwt = jwt.decode(a_jwt, SECRET_KEY, algorithms=utils.JWT_ALGORITHM)
        a_jwt2 = utils.make_jwt(user)
        assert a_jwt != a_jwt2

    # A JWT has basic JWT and the user uuid.
    assert set(decoded_jwt.keys()) == set(["uuid", "exp", "iat", "iss", "max-exp"])
    assert decoded_jwt["uuid"] == user.uuid
    assert utils.verify_jwt(user, a_jwt)

    # An expired JWT token will not be valid:
    with freeze_time("2020-06-01"):
        assert not utils.verify_jwt(user, a_jwt)

    # A JWT token can't be verified with the wrong secret
    assert not utils.verify_jwt(user, a_jwt, "bad secret")

    # A jwt with an expired max-exp is not valid.
    a_jwt = utils.make_jwt(user, datetime.now())
    with freeze_time("2020-04-02"):
        assert not utils.verify_jwt(user, a_jwt)


@freeze_time("2020-04-01")
def test_time_conversion(app):
    unix_time = utils._s_since_epoch(datetime.utcnow())
    assert datetime.utcnow().replace(tzinfo=timezone.utc) == utils.to_datetime(
        unix_time
    )

@patch("app.utils.boto3.client")
def test_get_s3(client_mock, app):
    assert utils.get_s3() is not None
    client_mock.assert_called()
