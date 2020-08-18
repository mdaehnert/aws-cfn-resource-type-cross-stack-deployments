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

    LOG.debug("Entering create.handle() method.")

    model.CrossStackId = str(uuid.uuid4())
    
    LOG.debug("Exiting create.handle() method.")

    progress.status = OperationStatus.SUCCESS
