from roles import queries
from app.model_utils import SystemPermissionEnum


def test_get_system_permission(app):
    perm = queries.get_system_permission(SystemPermissionEnum.PIPELINES_WORKER)
    assert perm.name == SystemPermissionEnum.PIPELINES_WORKER.name
    assert perm.code == SystemPermissionEnum.PIPELINES_WORKER.value

    # A second call works too!
    perm = queries.get_system_permission(SystemPermissionEnum.PIPELINES_WORKER)
    assert perm.name == SystemPermissionEnum.PIPELINES_WORKER.name
    assert perm.code == SystemPermissionEnum.PIPELINES_WORKER.value
