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
    LOG.info("Entering update.handle() method.")

    cfn_client = utils.get_cross_cfn_client(session, model, "UpdateHandler")

    if not callback_context.get("UPDATE_STARTED"):
        model.CfnStackId = "{}-{}-{}".format(model.CfnStackName, model.AccountId, model.Region)
        _update_stack(cfn_client, model)
        callback_context["UPDATE_STARTED"] = True

    if _is_update_complete(cfn_client, model):
        _set_output_values(cfn_client, model)
        progress.status = OperationStatus.SUCCESS

    LOG.info("Exiting update.handle() method.")


def _update_stack(cfn_client, model: ResourceModel):
    capabilities = [] if model.CfnCapabilities is None else model.CfnCapabilities

    cfn_input_parameters = {} if model.CfnParameters is None else model.CfnParameters
    final_parameters = []
    for key, value in cfn_input_parameters.items():
        final_parameters.append({
            "ParameterKey": key,
            "ParameterValue": value
        })
    try:
        request = {
            'StackName': model.CfnStackName,
            'Parameters': final_parameters,
            'Capabilities': capabilities
        }
        if model.CfnTemplateUrl is not None:
            request['TemplateURL'] = model.CfnTemplateUrl
        else:
            request['TemplateBody'] = model.CfnTemplate

        cfn_client.update_stack(**request)
    except botocore.exceptions.ClientError as e:
        if "No updates are to be performed" in e.response['Error']['Message']:
            LOG.info("No updates, skipping")
        else:
            raise e


def _is_update_complete(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )

    stack_status = describe_response["Stacks"][0]["StackStatus"]
    if stack_status.endswith("_FAILED") or stack_status.endswith("ROLLBACK_COMPLETE"):
        raise Exception("StackStatus={}, StackStatusReason={}".format(stack_status, describe_response["Stacks"][0]["StackStatusReason"]))
    elif stack_status in ["UPDATE_COMPLETE", "CREATE_COMPLETE", "IMPORT_COMPLETE"]:
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
        LOG.info(output)
        setattr(model, f"CfnStackOutput{index}", output["OutputValue"])
        index += 1
