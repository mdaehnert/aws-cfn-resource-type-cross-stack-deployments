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
    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    LOG.error("Entering delete.handle() method.")
    
    cfn_client = utils.get_cross_cfn_client(session, model, "CreateHandler")
    _delete_stack(cfn_client, model)

    progress.status = OperationStatus.SUCCESS
    LOG.debug("Exiting delete.handle() method.")
    

def _delete_stack(cfn_client, model: ResourceModel):
    cfn_client.delete_stack(
        StackName=model.CfnStackName
    )
    
    waiter = cfn_client.get_waiter("stack_delete_complete")
    
    waiter.wait(StackName=model.CfnStackName)
