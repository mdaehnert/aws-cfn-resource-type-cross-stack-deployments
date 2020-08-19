import logging
import uuid
from typing import Any, MutableMapping, Optional

from . import utils

from cloudformation_cli_python_lib import (
    ProgressEvent,
    SessionProxy,
    OperationStatus
)
from ..models import ResourceHandlerRequest, ResourceModel

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
    cfn_client = utils.get_cross_cfn_client(model, "CreateHandler")
    _create_stack(cfn_client, model)

    model.StackId = "{}-{}-{}".format(model.CfnStackName, model.AccountId, model.Region)

    progress.status = OperationStatus.SUCCESS
    LOG.debug("Exiting create.handle() method.")


def _create_stack(cfn_client, model: ResourceModel):
    capabilities = [] if model.CfnCapabilities is None else model.CfnCapabilities
    tags = [] if model.Tags is None else model.Tags

    create_response = cfn_client.create_stack(
        StackName=model.CfnStackName,
        TemplateBody=model.CfnTemplate,
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
    
    waiter = cfn_client.get_waiter("stack_create_complete")
    waiter.wait(StackName=model.CfnStackName)