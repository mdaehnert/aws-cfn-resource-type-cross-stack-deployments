import logging
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
    LOG.info("Entering create.handle() method.")
    
    cfn_client = utils.get_cross_cfn_client(session, model, "CreateHandler")
    
    if not callback_context.get("CREATE_STARTED"):
        model.CfnStackId = "{}-{}-{}".format(model.CfnStackName, model.AccountId, model.Region)
        _create_stack(cfn_client, model)
        callback_context["CREATE_STARTED"] = True
    
    if _is_create_complete(cfn_client, model):
        _set_output_values(cfn_client, model)
        progress.status = OperationStatus.SUCCESS

    LOG.info("Exiting create.handle() method.")


def _create_stack(cfn_client, model: ResourceModel):
    capabilities = [] if model.CfnCapabilities is None else model.CfnCapabilities
    tags = [] if model.Tags is None else model.Tags

    cfn_input_parameters = [] if model.CfnParameters is None else model.CfnParameters
    final_parameters = []
    for key, value in model.CfnParameters.items():
        final_parameters.append({
            "ParameterKey": key,
            "ParameterValue": value
        })

    cfn_client.create_stack(
        StackName=model.CfnStackName,
        TemplateBody=model.CfnTemplate,
        Parameters=final_parameters,
        Capabilities=capabilities,
        Tags=tags
    )
    
    
def _is_create_complete(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )
    
    stack_status = describe_response["Stacks"][0]["StackStatus"]
    if stack_status.endswith("_FAILED"):
        raise Exception("StackStatus={}, StackStatusReason={}".format(stack_status, describe_response["Stacks"][0]("StackStatusReason")))
    elif stack_status == "CREATE_COMPLETE":
        return True
    else:
        return False


def _set_output_values(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )
    
    outputs = describe_response["Stacks"][0]["Outputs"]
    # Clear from previous executions (Mostly interesting for UPDATE).
    model.CfnStackOutputs = {}

    index = 1
    for output in outputs:
        model.CfnStackOutputs[f"CfnStackOutput{index}"] = output["OutputValue"]
        index += 1