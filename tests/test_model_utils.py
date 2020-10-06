from application_roles.model_utils import get_db


def test_get_db_default():
    assert get_db() is not None


def test_get_db_bad_module():
    with pytest.raises(ModuleNotFoundError):
        get_db("avalu")


def test_get_db_bad_module():
    get_db("tests.sample_db") == "sample"
