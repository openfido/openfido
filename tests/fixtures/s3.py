import botocore.session

from pytest import fixture

@fixture(scope="function")
def s3_client():
    return botocore.session.get_session().create_client('s3')