import logging
import json
from typing import Any, MutableMapping

from cloudformation_cli_python_lib import (
    ProgressEvent,
    SessionProxy,
    OperationStatus
)

from . import utils
from ..models import ResourceHandlerRequest, ResourceModel


LOG = logging.getLogger(__name__)


def handle(
    session: SessionProxy,
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
    progress: ProgressEvent
):
    model = request.desiredResourceState
    LOG.setLevel(model.LogLevel)
    LOG.info("Entering list.handle() method.")
    
    cfn_client = utils.get_cross_cfn_client(session, model, "CreateHandler")

    progress.status = OperationStatus.SUCCESS
    LOG.info("Exiting list.handle() method.")
