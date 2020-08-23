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
        resourceModel=model,
        callbackContext=callback_context,
        callbackDelaySeconds=10
    )

    model.AssumeRolePath  = "/" if model.AssumeRolePath is None else model.AssumeRolePath
    model.LogLevel = logging.WARNING if model.LogLevel is None else model.LogLevel
    
    LOG.setLevel(model.LogLevel)
    _log_parameters(model, callback_context)

    try:
        if isinstance(session, SessionProxy):
            create.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
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
        resourceModel=model,
        callbackContext=callback_context,
        callbackDelaySeconds=10
    )

    model.AssumeRolePath  = "/" if model.AssumeRolePath is None else model.AssumeRolePath
    model.LogLevel = logging.WARNING if model.LogLevel is None else model.LogLevel

    LOG.setLevel(model.LogLevel)
    _log_parameters(model, callback_context)

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
        resourceModel=model,
        callbackContext=callback_context,
        callbackDelaySeconds=10
    )

    LOG.setLevel(model.LogLevel)
    _log_parameters(model, callback_context)

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
    
    LOG.error(request)

    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
        callbackContext=callback_context,
        callbackDelaySeconds=10
    )

    LOG.setLevel(model.LogLevel)
    LOG.info("Entering read.handle() method.")

    _log_parameters(model, callback_context)

    try:
        if isinstance(session, SessionProxy):
            read.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")

    LOG.info("Exiting read.handle() method.")
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
        resourceModel=model,
        callbackContext=callback_context,
        callbackDelaySeconds=10
    )

    LOG.setLevel(model.LogLevel)
    _log_parameters(model, callback_context)

    try:
        if isinstance(session, SessionProxy):
            listcfn.handle(session, request, callback_context, progress)
    except TypeError as e:
        raise exceptions.InternalFailure(f"was not expecting type {e}")
    return progress


def _log_parameters(model: ResourceModel, callback_context: MutableMapping[str, Any]):
    LOG.debug("Parameters:")
    LOG.debug("0. CallbackContext=%s", callback_context)
    LOG.debug("1. AccountId=%s", model.AccountId)
    LOG.debug("2. Region=%s", model.Region)
    LOG.debug("3. AssumeRolePath=%s", model.AssumeRolePath)
    LOG.debug("4. AssumeRoleName=%s", model.AssumeRoleName)
    LOG.debug("5. CfnStackName=%s", model.CfnStackName)
    LOG.debug("6. CfnCapabilities=%s", model.CfnCapabilities)
    LOG.debug("7. CfnTemplate=%s", model.CfnTemplate)
    LOG.debug("8. LogLevel=%s", model.LogLevel)
