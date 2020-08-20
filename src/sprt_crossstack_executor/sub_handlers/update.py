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
    
    cfn_client = utils.get_cross_cfn_client(session, model, "UpdateHandler")
    
    if not callback_context.get("UPDATE_STARTED"):
        model.CfnStackId = "{}-{}-{}".format(model.CfnStackName, model.AccountId, model.Region)
        _update_stack(cfn_client, model)
        callback_context["UPDATE_STARTED"] = True
    
    if _is_update_complete(cfn_client, model):
        progress.status = OperationStatus.SUCCESS

    LOG.debug("Exiting update.handle() method.")


def _update_stack(cfn_client, model: ResourceModel):
    capabilities = [] if model.CfnCapabilities is None else model.CfnCapabilities
    tags = [] if model.Tags is None else model.Tags

    cfn_client.create_stack(
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
    
    
def _is_update_complete(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )
    
    stack_status = describe_response["Stacks"][0]["StackStatus"]
    if stack_status.endswith("_FAILED"):
        raise Exception("StackStatus={}, StackStatusReason={}".format(stack_status, describe_response["Stacks"][0]("StackStatusReason")))
    elif stack_status == "UPDATE_COMPLETE":
        return True
    else:
        return False