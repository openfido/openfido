from ..model_utils import CommonColumnsMixin, get_db

db = get_db()


class Workflow(CommonColumnsMixin, db.Model):
    """ Represents a Workflow: a collection of connected pipelines. """

    __tablename__ = "workflow"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
