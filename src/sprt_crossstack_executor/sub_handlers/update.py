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
    LOG.error("Entering update.handle() method.")
    
    cfn_client = utils.get_cross_cfn_client(session, model, "CreateHandler")
    _update_stack(cfn_client, model)
    
    progress.status = OperationStatus.SUCCESS
    LOG.debug("Exiting update.handle() method.")


def _update_stack(cfn_client, model: ResourceModel):
    capabilities = [] if model.CfnCapabilities is None else model.CfnCapabilities
    tags = [] if model.Tags is None else model.Tags

    cfn_client.update_stack(
        StackName=model.CfnStackName,
        TemplateBody=json.dumps(model.CfnTemplate),
        # Parameters=[
        #     {
        #         'ParameterKey': 'string',
        #         'ParameterValue': 'string',
        #         'UsePreviousValue': True|False,
        #         'ResolvedValue': 'string'
        #     },
        # ],
        Capabilities=capabilities,
        # RoleARN='string',
        Tags=tags,
        # EnableTerminationProtection=True|False
    )
    
    
    waiter = cfn_client.get_waiter("stack_update_complete")
    
    waiter.wait(StackName=model.CfnStackName)
