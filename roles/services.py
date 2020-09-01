from .models import db, Application, ApplicationSystemPermission, SystemPermission
from .queries import get_system_permission


def create_application(name, permissions):
    # TODO support multiple permissions.
    application = Application(name=name)
    application_system_permission = ApplicationSystemPermission()
    system_permission = get_system_permission(permissions)
    system_permission.application_system_permissions.append(application_system_permission)
    application.application_system_permissions.append(application_system_permission)

    db.session.add(application)

    return application
