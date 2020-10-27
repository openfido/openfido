from application_roles import queries
from enum import IntEnum


class ExampleEnum(IntEnum):
    A_ROLE = 1


def test_get_system_permission(app):
    """Tests system permissions. """

    with app.app_context():
        perm = queries.get_system_permission(ExampleEnum.A_ROLE)
        assert perm.name == ExampleEnum.A_ROLE.name
        assert perm.code == ExampleEnum.A_ROLE.value

        # A second call works too!
        perm = queries.get_system_permission(ExampleEnum.A_ROLE)
        assert perm.name == ExampleEnum.A_ROLE.name
        assert perm.code == ExampleEnum.A_ROLE.value
