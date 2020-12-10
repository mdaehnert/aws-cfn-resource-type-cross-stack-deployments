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
    LOG.info("Entering delete.handle() method.")

    cfn_client = utils.get_cross_cfn_client(session, model, "DeleteHandler")

    if not callback_context.get("DELETE_STARTED"):
        _add_context_info(cfn_client, callback_context, model)
        _delete_stack(cfn_client, model)
        callback_context["DELETE_STARTED"] = True

    if _is_delete_complete(cfn_client, callback_context):
        progress.status = OperationStatus.SUCCESS

    LOG.info("Exiting delete.handle() method.")


def _add_context_info(cfn_client, callback_context: MutableMapping[str, Any], model: ResourceModel):
    """
        After a stack is deleted, it's only callable via StackId, but no longer via StackName.
        Therefore we collect the Id before starting to delete it. Used to ask StackStatus later on.
    """
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )

    callback_context["STACK_ID"] = describe_response["Stacks"][0]["StackId"]


def _delete_stack(cfn_client, model: ResourceModel):
    cfn_client.delete_stack(
        StackName=model.CfnStackName
    )


def _is_delete_complete(cfn_client, callback_context: MutableMapping[str, Any]):
    describe_response = cfn_client.describe_stacks(
        StackName=callback_context["STACK_ID"]
    )

    stack_status = describe_response["Stacks"][0]["StackStatus"]
    if stack_status.endswith("_FAILED"):
        raise Exception("StackStatus={}, StackStatusReason={}".format(stack_status, describe_response["Stacks"][0]("StackStatusReason")))
    elif stack_status == "DELETE_COMPLETE":
        return True
    else:
        return False
