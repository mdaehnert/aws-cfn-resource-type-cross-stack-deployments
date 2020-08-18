import logging
import uuid
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    ProgressEvent,
    SessionProxy,
    OperationStatus
)
from ..models import ResourceHandlerRequest

LOG = logging.getLogger(__name__)

def handle(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
    progress: ProgressEvent
):
    model = request.desiredResourceState
    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    LOG.error("Entering create.handle() method.")

    LOG.debug(model.CfnTemplate)
    

    model.CrossStackId = str(uuid.uuid4())
    progress.status = OperationStatus.SUCCESS
    LOG.debug("Exiting create.handle() method.")

