import logging
import uuid
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions
)

from .sub_handlers import (
    create,
    update,
    delete,
    read,
    listcfn
)

from .models import ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)

TYPE_NAME = "SPRT::CrossStack::Executor"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model
    )

    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    _log_parameters(model)

    try:
        if isinstance(session, SessionProxy):
            create.handle(session, request, callback_context, progress)
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")
    return progress


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any]
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model
    )

    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    _log_parameters(model)

    try:
        if isinstance(session, SessionProxy):
            update.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
    return progress


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any]
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model
    )

    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    _log_parameters(model)

    try:
        if isinstance(session, SessionProxy):
            delete.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any]
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model
    )

    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    _log_parameters(model)

    try:
        if isinstance(session, SessionProxy):
            read.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
    return progress


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any]
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model
    )

    LOG.setLevel(model.LogLevel if model.LogLevel is not None else logging.WARNING)
    _log_parameters(model)

    try:
        if isinstance(session, SessionProxy):
            listcnf.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
    return progress


def _log_parameters(model):
    LOG.debug("Parameters:")
    LOG.debug("1. AccountId=%s", model.AccountId)
    LOG.debug("2. Region=%s", model.Region)
    LOG.debug("3. AssumeRoleName=%s", model.AssumeRoleName)
    LOG.debug("4. LogLevel=%s", model.LogLevel)
    LOG.debug("END Parameters")
    