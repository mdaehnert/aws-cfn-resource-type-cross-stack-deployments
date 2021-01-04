import logging
from typing import Any, MutableMapping

import botocore
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

    cfn_input_parameters = {} if model.CfnParameters is None else model.CfnParameters
    final_parameters = []
    for key, value in cfn_input_parameters.items():
        final_parameters.append({
            "ParameterKey": key,
            "ParameterValue": value
        })

    stack_exists = False
    try:
        stacks = cfn_client.describe_stacks(
            StackName=model.CfnStackName
        )
        if len(stacks['Stacks']) > 0:
            stack_exists = True
            LOG.info("Stack exists, updating!")
    except botocore.exceptions.ClientError as e:
        if f"Stack with id {model.CfnStackName} does not exist" in e.response['Error']['Message']:
            LOG.info("Stack does not exist, creating new one")
            stack_exists = False
        else:
            raise e

    request = {
        'StackName': model.CfnStackName,
        'Parameters': final_parameters,
        'Capabilities': capabilities
    }
    if model.CfnTemplateUrl is not None:
        request['TemplateURL'] = model.CfnTemplateUrl
    else:
        request['TemplateBody'] = model.CfnTemplate

    if not stack_exists:
        cfn_client.create_stack(**request)
    else:
        try:
            cfn_client.update_stack(**request)
        except botocore.exceptions.ClientError as e:
            if "No updates are to be performed" in e.response['Error']['Message']:
                LOG.info("No updates, skipping")
            else:
                raise e


def _is_create_complete(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )

    stack_status = describe_response["Stacks"][0]["StackStatus"]
    if stack_status.endswith("_FAILED"):
        raise Exception("StackStatus={}, StackStatusReason={}".format(stack_status, describe_response["Stacks"][0]("StackStatusReason")))
    elif stack_status in ["CREATE_COMPLETE", "UPDATE_COMPLETE"]:
        return True
    else:
        return False


def _set_output_values(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )
    outputs = [] if 'Outputs' not in describe_response["Stacks"][0] else describe_response["Stacks"][0]["Outputs"]

    index = 1
    for output in outputs:
        setattr(model, f"CfnStackOutput{index}", output["OutputValue"])
        index += 1
