from flask import current_app

from application_roles.model_utils import get_db, CommonColumnsMixin

db = get_db()


class OrganizationPipeline(CommonColumnsMixin, db.Model):
    """ Represents a 'pipeline' job of a specific organization. """

    __tablename__ = "organization_pipeline"

    organization_uuid = db.Column(db.String(32), nullable=False, server_default="")
    pipeline_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
