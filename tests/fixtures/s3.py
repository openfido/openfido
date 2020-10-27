import botocore.session

from pytest import fixture

@fixture(scope="function")
def s3_client():
    """Stub s3 client fixture."""

    return botocore.session.get_session().create_client('s3')
