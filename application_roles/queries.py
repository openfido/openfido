from .models import db, Application, ApplicationSystemPermission, SystemPermission


def is_permitted(api_key, permission):
    """ Returns True when the Application associated with permission_code exists. """
    permission_subquery = (
        db.session.query(ApplicationSystemPermission.id)
        .join(SystemPermission)
        .filter(SystemPermission.code == permission.value)
        .subquery("permission_subquery")
    )
    application = (
        Application.query.join(Application.application_system_permissions)
        .filter(Application.api_key == api_key)
        .filter(
            Application.application_system_permissions.any(
                ApplicationSystemPermission.system_permission_id.in_(
                    permission_subquery
                )
            )
        )
    )

    return application.one_or_none() is not None


def get_system_permission(permission):
    """ Find a specific permission. """
    system_permission = SystemPermission.query.filter(
        SystemPermission.code == permission
    ).one_or_none()
    if system_permission is not None:
        return system_permission

    system_permission = SystemPermission(name=permission.name, code=permission.value)
    db.session.add(system_permission)

    return system_permission
