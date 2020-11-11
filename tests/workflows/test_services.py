from unittest.mock import patch

import io
import pytest
import responses
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.workflows.models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
    OrganizationWorkflowPipelineRun,
)
from app.workflows.services import (
    create_workflow,
    fetch_workflows,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import (
    ORGANIZATION_UUID,
    WORKFLOW_UUID,
)

WORKFLOW_JSON = {
  "created_at": "2020-11-11T03:19:32.401965",
  "description": "A workflow that does cool things2",
  "name": "My Workflow2",
  "updated_at": "2020-11-11T03:19:32.401973",
  "uuid": "da9917748b2f4d71bc82426579b7565c"
}