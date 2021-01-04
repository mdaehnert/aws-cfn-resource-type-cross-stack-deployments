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

    cfn_client = utils.get_cross_cfn_client(session, model, "ReadHandler")
    _set_output_values(cfn_client, model)

    progress.status = OperationStatus.SUCCESS


def _set_output_values(cfn_client, model: ResourceModel):
    describe_response = cfn_client.describe_stacks(
        StackName=model.CfnStackName
    )

    outputs = [] if 'Outputs' not in describe_response["Stacks"][0] else describe_response["Stacks"][0]["Outputs"]

    index = 1
    for output in outputs:
        if index == 10:
            raise Exception("Only 9 output variables are created so far.")

        setattr(model, f"CfnStackOutput{index}", output["OutputValue"])
        index += 1


    LOG.debug("Following variables were defined (CfnStackOutput*): %s", model)
