import pytest

from application_roles.model_utils import get_db


def test_get_db_default():
    """Tests db default. """

    assert get_db() is not None


def test_get_db_bad_module():
    """ Tests bad module. """

    with pytest.raises(ModuleNotFoundError):
        get_db("should_error")


def test_get_db_default_name():
    """Tests db default name. """

    assert get_db("tests.sample_db") == "sample"
